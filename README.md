# Single-Server Key–Value Store

A single-server HTTP key–value store built with Python, Flask, and SQLite. It implements **GET, PUT, and DEL** operations, supports concurrent requests, stores data persistently, and records timestamped operations.

## Features

- **PUT:** Create or replace the string value associated with a key.
- **GET:** Retrieve the value associated with a key.
- **DEL:** Delete a key and its value.
- **Persistence:** SQLite commits writes to a database file that can be reused after a server restart.
- **Concurrency:** Flask handles multiple requests; a process-local lock serializes writes and deletes.
- **Error handling:** JSON responses and HTTP status codes for invalid requests, missing keys, and database errors.
- **Logging:** Timestamped operation and error records.
- **Evaluation:** Functional tests, concurrent same-key tests, and throughput/latency benchmarks.

## Requirements

- Python 3.10 or newer
- pip
- Dependencies listed in `requirements.txt`

## Installation

Clone the repository and install dependencies:

```powershell
git clone https://github.com/Buddha-subedi/cloud-computing-kv-store.git
cd cloud-computing-kv-store
python -m pip install -r requirements.txt
```

## Running the Server

**Terminal 1 — start the server:**

```powershell
python server.py
```

By default, the server listens at `http://127.0.0.1:8080`. Keep this terminal open while running requests and tests. Press `Ctrl+C` to stop the server.

**Terminal 2 — open the same project folder:**

```powershell
cd C:\Users\User\cloud-computing-kv-store
```

The folder path above is an example; use the actual location of your extracted or cloned project.

## HTTP API

| Operation | HTTP method | Endpoint | Request body | Successful response |
|---|---|---|---|---|
| PUT | `PUT` | `/<key>` | `{"value":"hello"}` | `200 OK` with key and value |
| GET | `GET` | `/<key>` | None | `200 OK` with key and value |
| DEL | `DELETE` | `/<key>` | None | `200 OK` with deletion message |

**Example using Python Requests:**

```python
import requests

url = "http://127.0.0.1:8080/student1"

print(requests.put(url, json={"value": "hello"}).json())  # PUT
print(requests.get(url).json())                         # GET
print(requests.delete(url).json())                      # DEL
```

PUT is an **upsert**: it creates a missing key or replaces an existing value. Values must be strings supplied in a JSON object under the `value` field. Keys occupy a single URL path segment.

**Error handling:** Invalid PUT payloads return `400 Bad Request`; GET or DEL requests for missing keys return `404 Not Found`; database failures return `500 Internal Server Error`.

For compatibility with the provided benchmark, the server also accepts `POST /<key>` as an alias for the PUT operation. The primary API uses HTTP PUT.

## Tests and Demonstration

With the server running in Terminal 1, execute the following commands **one at a time in Terminal 2**:

```powershell
python test_server.py
python test_concurrency.py
python demo.py
python kv_bench.py
```

- `test_server.py` checks PUT, GET, DEL, updates, invalid values, and missing keys.
- `test_concurrency.py` tests 60 concurrent PUTs and 30 concurrent DELs targeting the same key with 12 workers.
- `demo.py` demonstrates the three key–value operations.
- `kv_bench.py` benchmarks 300 PUTs followed by 300 GETs using three client threads.
- `kv_bench_instructor.py` runs the supplied POST/GET benchmark against the compatibility endpoint.

## Performance Benchmark

Run both write and read phases:

```powershell
python kv_bench.py
```

The benchmark reports successful requests, errors, mismatches, throughput (operations/second), average latency, and P99 latency. It writes 300 key–value pairs and then reads the same 300 keys to verify their values.

A correct run should report `ok=300 mismatch=0 error=0` for each phase. Actual performance depends on the machine and runtime environment.

## Persistence Test

To test whether stored data remains available after stopping and restarting the server:

1. In **Terminal 2**, write the keys:

   ```powershell
   python kv_bench.py set
   ```

2. In **Terminal 1**, press `Ctrl+C` to stop the server, then restart it:

   ```powershell
   python server.py
   ```

3. In **Terminal 2**, read and verify the stored keys:

   ```powershell
   python kv_bench.py get
   ```

If the GET phase reports `ok=300 mismatch=0 error=0`, all expected values remained available after that controlled restart. Keep the same `kv_store.db` file and working directory for both server runs. This procedure does not test sudden power-loss recovery.

## Storage, Concurrency, and Logging

- `kv_store.db` is the SQLite database file created when the server starts. Its path can be overridden using the `KV_DB` environment variable.
- `kv_operations.log` records timestamped operations, status codes, and errors.
- Each database operation uses its own SQLite connection.
- PUT and DEL operations are serialized within the server process using `threading.Lock`; SQLite transactions commit updates atomically.
- If multiple clients PUT the same key, the final stored value is determined by the order in which writes commit.

## GitHub Codespaces

Open the repository in GitHub Codespaces. In the first terminal, start the server:

```bash
bash scripts/codespaces_server.sh
```

In a second terminal, run the demonstration and tests:

```bash
bash scripts/codespaces_demo.sh
```

The repository includes `.devcontainer/devcontainer.json` for the development environment.

## Project Files

| File | Purpose |
|---|---|
| `server.py` | Flask API, SQLite storage, concurrency control, and logging |
| `test_server.py` | Functional API tests |
| `test_concurrency.py` | Concurrent same-key PUT/DEL tests |
| `demo.py` | Short operation demonstration |
| `kv_bench.py` | PUT/GET throughput and latency benchmark |
| `kv_bench_instructor.py` | POST/GET compatibility benchmark |
| `REPORT.md` | Technical report |
| `DEMO_CHEATSHEET.md` | Demonstration instructions |
| `scripts/` | Windows and Codespaces helper scripts |

## Limitations and Future Work

This implementation is intended for a single local server process. It does not provide authentication, TLS, replication, or cross-process locking. Future improvements could include request-size limits, deployment with a production WSGI server, stronger stress testing, and distributed replication.
