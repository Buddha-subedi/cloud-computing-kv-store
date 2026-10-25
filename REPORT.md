# Single-Server Key–Value Store — Technical Report

## Design decisions and justification

I implemented a standalone key–value server in **Python using Flask** because Flask provides simple HTTP routing and supports concurrent requests. The API exposes **PUT** to insert or replace a string value, **GET** to retrieve it, and **DELETE (DEL)** to remove it. The server also accepts HTTP POST as a write alias because the provided benchmarking script uses POST for its SET phase. **SQLite** provides persistent, file-backed storage (`kv_store.db`) without a separate database service. Each request uses its own SQLite connection; transactions commit updates, and a process-local `threading.Lock` serializes writes and deletes to protect shared keys. Timestamped operation logs and JSON error responses support diagnosis and testing.

## Implementation challenges and solutions

**Concurrent updates:** Multiple clients may write to or delete the same key at once. I used a lock around modifying operations and SQLite transactions to avoid conflicting updates within the single server process. **Benchmark compatibility:** The specified PUT operation differs from the supplied benchmark's POST request; accepting both methods preserves the required PUT interface and allows the provided benchmark to run. **Execution setup:** The server must remain running in one terminal while tests run from the project directory in a second terminal. File-backed SQLite storage avoids losing committed records when the application process stops normally.

## Assumptions

The system runs as **one trusted local server process** at `127.0.0.1:8080`. Keys are single URL path segments; values are strings in a JSON `value` field. PUT creates or replaces a key. Missing keys return HTTP 404 and invalid PUT input returns HTTP 400. Concurrent writes to the same key are atomic, but the last committed value depends on scheduling. The application is not designed for public internet exposure or multiple independent server processes.

## Testing and benchmark results

The Windows PowerShell tests shown in the accompanying run passed: `test_server.py` verified PUT, GET, update, DELETE, validation, and missing-key handling; `test_concurrency.py` passed **60 concurrent PUTs and 30 concurrent DELETEs on one key**. `demo.py` returned successful HTTP 200 responses for PUT/GET/update/DELETE and HTTP 404 for a missing key.

The **PUT/GET benchmark** used **3 client threads and 300 keys** (`key_0`–`key_299`), with the following observed results:

| Metric | PUT / SET | GET |
|---|---:|---:|
| Successful requests | 300 | 300 |
| Mismatches / errors | 0 / 0 | 0 / 0 |
| Elapsed time | 1.14 s | 1.06 s |
| Throughput | 262.1 ops/s | 283.1 ops/s |
| Average latency | 11.41 ms | 10.55 ms |
| P99 latency | 32.55 ms | 30.75 ms |

**Total:** 600 successful requests in **2.20 s** (**272.2 ops/s**). A subsequent standalone GET phase retrieved **300/300 values**, with **0 mismatches and 0 errors**, in **1.11 s** (**269.9 ops/s**, average **11.09 ms**, P99 **30.88 ms**). This confirms read-back correctness, **not** persistence across a restart: the supplied screenshots do not show the server being stopped between SET and GET. To verify restart persistence, run `python kv_bench.py set`, stop and restart `python server.py` without deleting `kv_store.db`, then run `python kv_bench.py get`.

## Limitations and future improvements

The process-local lock does not coordinate multiple server processes, and the Flask development server is not production-grade. Future work could add authentication and TLS, request-size limits, a production WSGI server, more extensive load and crash-recovery testing, cross-process coordination, and replication for fault tolerance.
