# Single-Server Key–Value Store — Coding Assignment 1

A standalone Python/Flask HTTP server with SQLite persistence, concurrent request handling, timestamped operation logs, and GET/PUT/DELETE endpoints. Designed for **local Windows PowerShell** at `127.0.0.1:8080`. No MSI/Agate or paid cloud host required.

## What the instructor requires

The original assignment describes GET, PUT, DEL, concurrency, logging, error handling, and optional persistence. The instructor subsequently clarified that **GET and PUT are sufficient for full credit on Coding Assignment 1** and the benchmark is for later assignments. This project implements the additional features anyway. The benchmark is provided for optional validation. Submit the source repository, a one-page report, and be ready to demonstrate the program.

## Files

- `server.py` — Flask HTTP API, SQLite database, write lock, and logs
- `test_server.py` — functional test (GET/PUT/DELETE/missing key)
- `test_concurrency.py` — concurrent writes and deletes
- `kv_bench.py` — 3-thread, 300-key write/read benchmark compatible with the supplied protocol
- `demo.py` — short demonstration using requests
- `requirements.txt` — Flask and requests
- `REPORT_TEMPLATE.md` — **customize before submission**, including your own test observations
- `.gitignore` — excludes local database, logs, Python cache, and environments

## Quick start — Windows PowerShell

1. Extract the ZIP. Open PowerShell in the folder containing `server.py`. For example:

   ```powershell
   cd "C:\Users\subed042\Downloads\kv_assignment"
   dir
   ```

2. Install dependencies (once):

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. **Terminal 1:** start the server and leave it running:

   ```powershell
   python -u server.py
   ```

   Flask normally stays running and does not return to the prompt. That is **expected**, not a freeze. To stop it, press `Ctrl+C`.

4. **Terminal 2:** open another PowerShell window in the **same folder**:

   ```powershell
   python test_server.py
   python test_concurrency.py
   python demo.py
   python kv_bench.py
   ```

   The server must remain running in Terminal 1. If a test reports a connection error, check `Test-NetConnection 127.0.0.1 -Port 8080`.

## HTTP API

| Operation | HTTP request | Example response | Status |
|---|---|---|---|
| PUT | `POST /student1` with JSON `{"value":"Buddha"}` | `{"key":"student1","value":"Buddha"}` | 200 |
| GET | `GET /student1` | `{"key":"student1","value":"Buddha"}` | 200 |
| DEL | `DELETE /student1` | `{"message":"Deleted","key":"student1"}` | 200 |
| Missing key | `GET /unknown` | `{"error":"Key not found"}` | 404 |
| Invalid PUT | `POST /student1` without valid string `value` | JSON error | 400 |

**PowerShell example:**

```powershell
$body = @{ value = "Buddha" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8080/student1" -Method Post -ContentType "application/json" -Body $body
Invoke-RestMethod -Uri "http://127.0.0.1:8080/student1" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8080/student1" -Method Delete
```

The benchmark uses `POST /key_0` and expects `GET /key_0` to return JSON containing `"value":"value_0"`.

## Persistence demonstration (restart test)

In Terminal 2 run `python kv_bench.py set` (writes 300 keys). In Terminal 1 press `Ctrl+C`, then restart `python -u server.py`. In Terminal 2 run `python kv_bench.py get`. Expected **correctness target**: `ok=300 mismatch=0 error=0`. Actual latency and throughput depend on your computer. **Do not claim these results until you run the test.** The file `kv_store.db` must stay in the same working directory between restarts.

## Concurrency and design

Flask's threaded server can serve concurrent HTTP requests. Each database operation uses a separate SQLite connection. A Python `threading.Lock` serializes PUT/DELETE operations within this one process, and SQLite transactions commit each write. Concurrent writes to the same key are atomic, but the **last completed write wins**; the exact winning writer is nondeterministic. SQLite provides persistence without a separate database server. GET reads the committed state. This is a learning/demo server, **not a production internet-facing deployment**.

## Logs and errors

Operation timestamps and outcomes are written to `kv_operations.log` in the working directory. SQLite data is saved in `kv_store.db`. Missing keys return HTTP 404; malformed PUT values return 400; database failures return 500 without exposing internal details. No authentication or TLS is implemented, so bind to localhost only.

## Short demo (2–3 minutes)

1. Show Terminal 1 running `python -u server.py` on `127.0.0.1:8080`.
2. In Terminal 2 run `python demo.py`; explain PUT, GET, DELETE, and missing-key 404.
3. Run `python test_concurrency.py`; explain the write lock and SQLite transactions.
4. Open `kv_operations.log` and show timestamped operations.
5. Optionally run the set/restart/get persistence demonstration or benchmark.
6. Explain design choices and limitations using the one-page report.

## GitHub submission checklist

1. Run all tests locally and record **your own** results.
2. Edit `REPORT_TEMPLATE.md` to describe **what you actually did**, including any challenges you encountered; convert it to PDF if your instructor prefers.
3. Create a GitHub repository, upload source and report, and ensure the README is visible.
4. Share the repository with GitHub username `chalianwar` (invite as collaborator if private) and submit the URL through the course's requested channel.
5. Do not commit `kv_store.db`, logs, secrets, or virtual environments.

## Assumptions / limits

- Single local server process; no replication, authentication, TLS, or remote cloud deployment.
- Keys are one nonempty URL path segment; values are strings in JSON.
- POST is used as PUT semantics because the instructor's benchmark sends POST.
- GET after a successful completed POST returns the most recently committed value unless another client modifies the key.
- `kv_bench.py` included here follows the instructor's supplied protocol; use the latest Canvas file as authoritative if the instructor changes it.
