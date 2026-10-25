"""Concurrent PUT and DEL requests on the same key; run server.py first."""
from concurrent.futures import ThreadPoolExecutor
import requests

BASE = "http://127.0.0.1:8080/concurrent_test"

def write(i):
    response = requests.put(BASE, json={"value": f"writer_{i}"}, timeout=10)
    response.raise_for_status()

def remove(_):
    response = requests.delete(BASE, timeout=10)
    assert response.status_code in (200, 404), response.text

with ThreadPoolExecutor(max_workers=12) as pool:
    list(pool.map(write, range(60)))
response = requests.get(BASE, timeout=10)
assert response.status_code == 200, response.text
assert response.json()["value"] in {f"writer_{i}" for i in range(60)}
with ThreadPoolExecutor(max_workers=12) as pool:
    list(pool.map(remove, range(30)))
assert requests.get(BASE, timeout=10).status_code == 404
print("PASS: 60 concurrent PUTs and 30 concurrent DELs on one key")
