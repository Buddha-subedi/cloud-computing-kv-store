# Demonstration cheat sheet (2–3 minutes)

**What “be ready to provide a short demonstration” means:** You may be asked to **run your program live**, show that it stores/retrieves/deletes a value, and briefly explain your implementation. It does **not** necessarily mean you must submit a video. Ask the instructor if they require a recording.

1. Open PowerShell A: `cd "C:\Users\subed042\Downloads\kv_assignment"` then `python -u server.py`.
2. Open PowerShell B in the same directory: `python demo.py`.
3. Point out the successful PUT and GET, update, DELETE, and expected 404 for missing key.
4. Run `python test_concurrency.py` and explain: “A lock serializes modifying operations; SQLite commits changes transactionally.”
5. Show the log: `Get-Content .\kv_operations.log -Tail 10`.
6. Optional: `python kv_bench.py set`; restart server; `python kv_bench.py get`.

**Likely questions:**

- **Why Flask?** Lightweight HTTP routing with little setup.
- **Why SQLite?** Durable storage without installing a database server.
- **What is a key–value store?** A mapping from a unique key to its associated value.
- **What happens if a key is missing?** GET returns 404 and a JSON error.
- **How do you avoid concurrent-write corruption?** Lock around writes/deletes plus SQLite transactions.
- **Does a value survive restart?** Yes, if committed to the same SQLite file; verify with set/restart/get.
- **What does localhost mean?** The service accepts connections from the same computer, not the public internet.
- **What is throughput?** Successful requests per second; latency is time per request.
