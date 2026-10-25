# Demonstration quick reference

1. Install: `python -m pip install -r requirements.txt`.
2. Start server in Terminal 1: `python server.py`.
3. In Terminal 2: `python demo.py` — demonstrate PUT, GET, update, DEL and 404.
4. Run `python test_server.py` and `python test_concurrency.py`.
5. Run `python kv_bench.py` (PUT + GET benchmark).
6. Run `python kv_bench_instructor.py` (unchanged instructor POST + GET benchmark).
7. Show `kv_operations.log` for timestamps and `kv_store.db` for persistent storage.
8. Restart test: `python kv_bench.py set`, stop/restart server, `python kv_bench.py get`.

Explain that PUT is the primary write method and POST is supported only for compatibility with the supplied benchmark. This is a local single-process server.
