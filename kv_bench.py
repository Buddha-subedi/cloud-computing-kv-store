"""Benchmark standard HTTP PUT and GET; optionally test restart durability.
Usage: python kv_bench.py [set] [get]
"""
import queue
import sys
import threading
import time
import requests

BASE_URL = 'http://127.0.0.1:8080'
NUM_THREADS = 3
OPS_PER_THREAD = 100
NUM_KEYS = NUM_THREADS * OPS_PER_THREAD
PRINT_INTERVAL = 3
MAX_LOGGED_PROBLEMS = 5
_local = threading.local()
_log_lock = threading.Lock()
_logged = 0


def log_problem(message):
    global _logged
    with _log_lock:
        _logged += 1
        if _logged <= MAX_LOGGED_PROBLEMS:
            print(message)
        elif _logged == MAX_LOGGED_PROBLEMS + 1:
            print('  (further errors/mismatches suppressed; see counts in results)')


def session():
    if not hasattr(_local, 'session'):
        _local.session = requests.Session()
    return _local.session


def kv_store_operation(op_type, key, value):
    try:
        if op_type == 'set':
            response = session().put(f'{BASE_URL}/{key}', json={'value': value}, timeout=10)
            response.raise_for_status()
            return 'ok'
        if op_type == 'get':
            response = session().get(f'{BASE_URL}/{key}', timeout=10)
            response.raise_for_status()
            got = response.json().get('value')
            if got == value:
                return 'ok'
            log_problem(f'Mismatch on get {key!r}: expected {value!r}, got {got!r}')
            return 'mismatch'
        raise ValueError(f'Invalid operation: {op_type}')
    except Exception as exc:
        log_problem(f'Error during {op_type} for {key!r}: {exc}')
        return 'error'


class PhaseStats:
    def __init__(self):
        self.lock = threading.Lock()
        self.latencies = []
        self.mismatch = 0
        self.error = 0


def worker(tasks, stats, barrier):
    barrier.wait()
    while True:
        try:
            op, key, value = tasks.get_nowait()
        except queue.Empty:
            return
        start = time.perf_counter()
        result = kv_store_operation(op, key, value)
        elapsed = time.perf_counter() - start
        with stats.lock:
            if result == 'ok':
                stats.latencies.append(elapsed)
            elif result == 'mismatch':
                stats.mismatch += 1
            else:
                stats.error += 1


def monitor(stats, stop):
    seen, last = 0, time.perf_counter()
    while not stop.wait(PRINT_INTERVAL):
        with stats.lock:
            window = stats.latencies[seen:]
        now = time.perf_counter()
        if window:
            print(f'  [last {now-last:.1f}s] {len(window)/(now-last):.1f} ops/s, '
                  f'avg latency {1000*sum(window)/len(window):.2f} ms')
        seen += len(window)
        last = now


def run_phase(op_type):
    tasks = queue.Queue()
    for i in range(NUM_KEYS):
        tasks.put((op_type, f'key_{i}', f'value_{i}'))
    stats = PhaseStats()
    barrier = threading.Barrier(NUM_THREADS + 1)
    stop = threading.Event()
    workers = [threading.Thread(target=worker, args=(tasks, stats, barrier))
               for _ in range(NUM_THREADS)]
    watcher = threading.Thread(target=monitor, args=(stats, stop), daemon=True)
    for thread in workers:
        thread.start()
    watcher.start()
    barrier.wait()
    start = time.perf_counter()
    for thread in workers:
        thread.join()
    elapsed = time.perf_counter() - start
    stop.set()
    watcher.join()
    return stats, elapsed


def report(name, stats, elapsed):
    latencies = sorted(stats.latencies)
    ok = len(latencies)
    avg = 1000 * sum(latencies) / ok if ok else float('nan')
    p99 = 1000 * latencies[int(.99 * (ok - 1))] if ok else float('nan')
    print(f'{name}: ok={ok} mismatch={stats.mismatch} error={stats.error} '
          f'time={elapsed:.2f}s throughput={ok/elapsed:.1f} ops/s '
          f'avg={avg:.2f} ms p99={p99:.2f} ms')
    return ok


if __name__ == '__main__':
    phases = sys.argv[1:] or ['set', 'get']
    if any(p not in ('set', 'get') for p in phases):
        sys.exit('usage: python kv_bench.py [set] [get]')
    results = {}
    for phase in phases:
        print(f'Running {phase} phase on {NUM_KEYS} keys with {NUM_THREADS} threads...')
        results[phase] = run_phase(phase)
    print('\nFinal Results:')
    total_ok = 0
    total_time = 0
    for phase, (stats, elapsed) in results.items():
        total_ok += report(phase.upper(), stats, elapsed)
        total_time += elapsed
    print(f'TOTAL: {total_ok} successful ops in {total_time:.2f}s '
          f'({total_ok/total_time:.1f} ops/s)')
