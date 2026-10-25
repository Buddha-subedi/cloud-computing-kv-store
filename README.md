
# Single-Server Key–Value Store

A Python-based HTTP key–value storage system built with Flask and SQLite. The application supports persistent storage, concurrent client requests, GET/POST/DELETE operations, error handling, timestamped logging, and performance benchmarking.

## Features

- **Key–Value Operations:** Create, retrieve, update, and delete key–value pairs.
- **Persistent Storage:** SQLite maintains data across server restarts.
- **Concurrent Requests:** Multithreaded HTTP server with synchronized database writes.
- **Error Handling:** JSON responses with appropriate HTTP status codes.
- **Logging:** Timestamped records of operations and database errors.
- **Testing:** Functional and concurrency tests.
- **Benchmarking:** Throughput, average latency, and P99 latency measurements.

## Technology Stack

- Python
- Flask
- SQLite
- Requests
- Python Threading

## Project Structure

```text
cloud-computing-kv-store/
├── server.py
├── test_server.py
├── test_concurrency.py
├── kv_bench.py
├── demo.py
├── requirements.txt
├── README.md
├── REPORT_TEMPLATE.md
├── .gitignore
├── .devcontainer/
│   └── devcontainer.json
└── scripts/
    ├── windows_setup.ps1
    ├── windows_server.ps1
    ├── windows_demo.ps1
    ├── windows_persistence_set.ps1
    ├── windows_persistence_get.ps1
    ├── codespaces_setup.sh
    ├── codespaces_server.sh
    └── codespaces_demo.sh
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Buddha-subedi/cloud-computing-kv-store.git
cd cloud-computing-kv-store
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Server

Start the Flask application:

```bash
python server.py
```

The server listens at:

```text
http://127.0.0.1:8080
```

Keep the server running while executing client requests and tests in another terminal.

Press `Ctrl+C` to stop the server.

## HTTP API

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Create / Update | POST | `/<key>` | Store or update a value |
| Retrieve | GET | `/<key>` | Retrieve a stored value |
| Delete | DELETE | `/<key>` | Remove a stored key |

### Create or Update a Key

**Request:**

```http
POST /student1
Content-Type: application/json

{"value": "example_value"}
```

**Response (200 OK):**

```json
{
  "key": "student1",
  "value": "example_value"
}
```

### Retrieve a Key

**Request:**

```http
GET /student1
```

**Response (200 OK):**

```json
{
  "key": "student1",
  "value": "example_value"
}
```

### Delete a Key

**Request:**

```http
DELETE /student1
```

**Response (200 OK):**

```json
{
  "key": "student1",
  "message": "Deleted"
}
```

### Error Responses

| HTTP Status | Meaning |
|-------------|---------|
| 200 | Successful operation |
| 400 | Invalid JSON or value |
| 404 | Key not found |
| 500 | Database error |

## Testing

Start the server in one terminal and execute the following commands in a second terminal.

### Functional Tests

```bash
python test_server.py
```

Verifies key insertion, retrieval, updates, deletion, and missing-key handling.

### Concurrency Tests

```bash
python test_concurrency.py
```

Tests concurrent access using 12 worker threads, including 60 write requests and 30 delete requests targeting the same key.

### Demonstration

```bash
python demo.py
```

Demonstrates the supported HTTP operations and server responses.

## Performance Benchmarking

Run:

```bash
python kv_bench.py
```

The benchmark uses:

- 3 concurrent client threads
- 300 unique keys
- 300 POST requests
- 300 GET requests
- 600 total requests

The GET phase verifies that retrieved values match the values written during the POST phase.

### Benchmark Results

Measured in GitHub Codespaces using three concurrent client threads:

| Metric | POST (SET) | GET |
|--------|-----------:|----:|
| Successful requests | 300 | 300 |
| Mismatches | 0 | 0 |
| Errors | 0 | 0 |
| Execution time | 0.77 s | 0.70 s |
| Throughput | 387.6 ops/s | 429.2 ops/s |
| Average latency | 7.71 ms | 6.96 ms |
| P99 latency | 16.96 ms | 14.70 ms |

**Overall:** 600 successful operations in approximately 1.47 seconds, with an aggregate throughput of 407.3 operations per second.

Performance varies depending on the execution environment and system workload.

## Persistence Testing

SQLite stores key–value pairs in `kv_store.db`.

To test persistence across server restarts:

**Step 1:** Start the server and write 300 keys.

```bash
python kv_bench.py set
```

**Step 2:** Stop the server using `Ctrl+C`, then restart it.

```bash
python server.py
```

**Step 3:** Retrieve and verify the stored values.

```bash
python kv_bench.py get
```

A successful test returns 300 correct values with zero errors or mismatches.

## GitHub Codespaces

The project includes a development container configuration for GitHub Codespaces.

1. Open the GitHub repository.
2. Select **Code → Codespaces → Create codespace on main**.
3. Open the integrated terminal.

**Terminal 1 — Start Server**

```bash
bash scripts/codespaces_server.sh
```

**Terminal 2 — Run Tests**

```bash
bash scripts/codespaces_demo.sh
```

To install dependencies manually:

```bash
bash scripts/codespaces_setup.sh
```

## Windows PowerShell

The application can also run locally on Windows.

**Terminal 1:**

```powershell
python -m pip install -r requirements.txt
python server.py
```

**Terminal 2:**

```powershell
python test_server.py
python test_concurrency.py
python demo.py
python kv_bench.py
```

Alternatively, use the provided PowerShell scripts.

## System Design

The application follows a client–server architecture.

1. **HTTP Client:** Sends GET, POST, and DELETE requests.
2. **Flask Server:** Processes requests, validates input, and returns JSON responses.
3. **SQLite Database:** Stores key–value pairs persistently.

### Concurrency

Flask supports multithreaded request handling. A Python `threading.Lock` serializes write and delete operations within the server process.

Each database operation uses a separate SQLite connection. SQLite transactions provide atomic commits and rollback behavior.

When multiple clients update the same key, the final value depends on the order of completed writes.

### Data Storage

The database contains a `kv` table with two columns:

| Column | Type | Description |
|--------|------|-------------|
| `key` | TEXT PRIMARY KEY | Unique key identifier |
| `value` | TEXT NOT NULL | Associated string value |

### Logging

Operations and errors are recorded in:

```text
kv_operations.log
```

The log includes timestamps, operation types, keys, and HTTP status codes.

## Limitations and Future Improvements

- Designed for a single server process.
- No distributed replication or fault tolerance.
- No authentication or TLS.
- Supports string values and single-segment URL keys.
- Uses Flask's development server for local testing.
- Potential extensions include distributed deployment, connection pooling, authentication, and more extensive performance testing.

## Repository

https://github.com/Buddha-subedi/cloud-computing-kv-store
