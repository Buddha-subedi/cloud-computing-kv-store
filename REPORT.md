# Single-Server Key–Value Store — Technical Report

## Design decisions and justification

The application is implemented in Python with Flask for its straightforward HTTP routing and SQLite for durable, file-backed key–value storage. The primary API exposes **PUT** to create/update, **GET** to retrieve, and **DELETE (DEL)** to remove entries. HTTP POST is accepted as an additional write alias for compatibility with the supplied benchmark. A SQLite table with a unique text primary key prevents duplicate keys. Each request uses its own database connection and transaction; a `threading.Lock` serializes write/delete sections within the single server process. Flask handles requests using threads. Logging records operation types, keys, outcomes, and timestamps.

## Implementation challenges and solutions

Concurrent modifications to a shared key can cause races, so write and delete operations are protected by a lock and committed using SQLite transactions. The benchmark uses POST for writes although the API requirement names PUT; both methods are supported while PUT remains the primary interface. Running a client against a stopped server causes connection errors; server and client are run in separate terminals. Persistence is implemented with a file-backed SQLite database rather than volatile in-memory storage.

## Assumptions

One trusted local server process listens on `127.0.0.1:8080`. Keys are single URL path segments, values are strings supplied in JSON, and PUT replaces any existing value. A missing key returns 404; invalid input returns 400. Concurrent writes are atomic, but their completion order is nondeterministic. The application is not intended for public production exposure.

## Validation

The repository includes functional tests, a same-key concurrency test, and a PUT/GET benchmark (3 threads, 300 keys per phase). The instructor-provided POST/GET benchmark is retained separately. Historical results from the earlier POST implementation showed 300/300 successful writes/reads and zero errors or mismatches in Codespaces; **re-run the tests after installing this revised version and record the new results before submission**. A restart check is available by running the SET phase, restarting the server, and running the GET phase.

## Future improvements

Add authentication and TLS, request size limits, stronger concurrency/load tests, multi-process coordination, monitoring, and replication/fault tolerance.
