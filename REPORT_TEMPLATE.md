# Coding Assignment 1 — Single-Server Key–Value Store

**Student:** [Your name]  
**Course:** [Course identifier]  
**Date:** [Date]

## Design decisions and justification

I implemented a single-server key–value store using Python 3, Flask, and SQLite. Flask exposes `POST /<key>` for PUT, `GET /<key>` for retrieval, and `DELETE /<key>` for removal. These routes match the provided benchmark protocol. SQLite stores `(key, value)` pairs in a local database file, so committed values persist across server restarts. The server listens on `127.0.0.1:8080`, which avoids the need for external hosting. Flask handles concurrent HTTP requests using threads. A process-level lock serializes writes/deletes, while SQLite transactions make each database modification atomic. Operations and outcomes are recorded in a timestamped log.

## Challenges and solutions

[Replace this paragraph with **your actual experience**. Example topics: setting up Python dependencies on Windows; understanding why the server keeps running without returning to the prompt; distinguishing localhost from the MSI login node; ensuring a second PowerShell window runs the client tests; validating persistence after restart. Do not claim a challenge you did not encounter.]

## Assumptions

The system runs as one trusted local process and is not publicly exposed. Keys are single URL path segments; values are JSON strings. PUT overwrites an existing key. A missing key returns HTTP 404, malformed input returns 400, and concurrent writes follow last-committed-write-wins behavior.

## Testing and results

Functional tests: [insert actual output]. Concurrency test: [insert actual output]. Benchmark (optional): SET [ok/mismatch/error, throughput, avg, p99]; GET [same]. Restart persistence test: [actual result or “not tested”]. Do not enter expected counts as if they were measurements.

## Future improvements

Possible extensions include authenticated clients, TLS, input size limits, connection pooling, a production WSGI server, richer performance tests, and replication across multiple servers.

*Edit to fit one page before submission; remove all bracketed instructions.*
