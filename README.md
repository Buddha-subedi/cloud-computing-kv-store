# Single-Server Key–Value Store

A Python/Flask single-server key–value store with **GET, PUT, and DEL** operations, SQLite persistence, concurrent request handling, error responses, and timestamped logs. Designed for local execution and GitHub Codespaces.

## Features

- **PUT** (`HTTP PUT /<key>`): create or replace a string value.
- **GET** (`HTTP GET /<key>`): retrieve a stored value.
- **DEL** (`HTTP DELETE /<key>`): remove a key and its value.
- SQLite database transactions preserve committed data across restarts.
- Flask handles concurrent requests; a process-local lock coordinates writes and deletes.
- JSON errors and HTTP status codes for missing keys, invalid input, and database failures.
- Timestamped logging and correctness, concurrency, and performance tests.

**Protocol compatibility:** The supplied benchmark uses HTTP `POST` for its logical write/SET operation. This server additionally accepts `POST /<key>` as an alias for PUT so that benchmark works unchanged. **The primary documented API and all main tests use HTTP PUT.**

## Requirements

Python 3.10+ and pip. Dependencies are listed in `requirements.txt`.

## Install and run

```bash
 git clone https://github.com/Buddha-subedi/cloud-computing-kv-store.git
 cd cloud-computing-kv-store
 python -m pip install -r requirements.txt
 python server.py
```

The server listens at `http://127.0.0.1:8080`. Leave it running and open a **second terminal** for the commands below. Stop it using `Ctrl+C`.

## API

| Operation | HTTP request | JSON request body | Success | Missing/invalid |
|---|---|---|---|---|
| **PUT** | `PUT /student1` | `{"value":"example"}` | `200`, key and value | `400` for invalid JSON/value |
| **GET** | `GET /student1` | None | `200`, key and value | `404` |
| **DEL** | `DELETE /student1` | None | `200`, deleted message | `404` |

Example with Python Requests:

```python
import requests
url = "http://127.0.0.1:8080/student1"
print(requests.put(url, json={"value": "hello"}).json())  # PUT
print(requests.get(url).json())                          # GET
print(requests.delete(url).json())                       # DEL
```

The PUT operation is an *upsert*: it inserts a missing key and replaces the value of an existing key. Values must be JSON strings, including the empty string if desired. Keys must fit a single URL path segment.

## Testing and demonstration

With the server running in Terminal 1, run in Terminal 2:

```bash
python test_server.py
python test_concurrency.py
python demo.py
python kv_bench.py
```

- `test_server.py`: GET, PUT, DEL, updates, invalid input and missing-key responses.
- `test_concurrency.py`: 60 concurrent PUTs and 30 concurrent DELs to the same key using 12 workers.
- `demo.py`: short GET/PUT/DEL demonstration.
- `kv_bench.py`: **HTTP PUT** benchmark (3 threads, 300 writes, 300 reads).
- `kv_bench_instructor.py`: unmodified supplied **HTTP POST** benchmark for protocol compatibility.

Benchmark phases can be run separately:

```bash
python kv_bench.py set
# Stop and restart server in Terminal 1, retaining the same database file.
python kv_bench.py get
```

The expected correctness target is `ok=300 mismatch=0 error=0` for each phase. This tests data availability after a controlled restart; it does not establish power-loss durability.

### Previously measured benchmark (original POST protocol)

A previous GitHub Codespaces run of the original POST-based benchmark reported 300 successful writes and 300 successful reads with zero errors/mismatches. Write throughput was 387.6 ops/s (average 7.71 ms; P99 16.96 ms), and read throughput was 429.2 ops/s (average 6.96 ms; P99 14.70 ms). **These are historical results from the earlier implementation, not measurements of this revised PUT-based package.** Re-run the benchmarks for current results.

## Storage, synchronization and logging

- `kv_store.db`: SQLite database file, generated at runtime; default path can be overridden using `KV_DB`.
- `kv_operations.log`: timestamped operations and errors, generated at runtime.
- Every request opens and closes its own SQLite connection; writes use transactions and a `threading.Lock`.
- Simultaneous writes to the same key are atomic; the final value depends on which write commits last.
- Missing keys return HTTP 404, invalid PUT bodies return HTTP 400, and database failures return HTTP 500.

## Windows PowerShell

In two PowerShell terminals, run:

```powershell
# Terminal 1
python -m pip install -r requirements.txt
python server.py
```

```powershell
# Terminal 2
python test_server.py
python test_concurrency.py
python demo.py
python kv_bench.py
```

Helper scripts are also available under `scripts/`.

## GitHub Codespaces

Create a Codespace from the repository and use the Bash terminal. Run `bash scripts/codespaces_server.sh` in Terminal 1 and `bash scripts/codespaces_demo.sh` in Terminal 2. A `.devcontainer/devcontainer.json` configuration is included.

## Project files

| File | Purpose |
|---|---|
| `server.py` | Flask GET/PUT/DEL server with SQLite, locks, and logging |
| `test_server.py` | Functional API tests |
| `test_concurrency.py` | Same-key concurrent PUT/DEL tests |
| `demo.py` | Short interactive demonstration |
| `kv_bench.py` | PUT/GET throughput and latency benchmark |
| `kv_bench_instructor.py` | Original POST/GET benchmark, unchanged |
| `REPORT.md` | Concise technical report |
| `DEMO_CHEATSHEET.md` | Demo steps |
| `scripts/` | Windows and Codespaces helper scripts |

## Limitations and future work

This is a single-process local development server, not a production internet-facing service. It does not implement authentication, TLS, replication, or cross-process locking. Potential improvements include request size limits, a production WSGI server, stronger load testing, and distributed storage/replication.
