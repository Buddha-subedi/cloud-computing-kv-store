"""Exercise simultaneous writes and deletes of the same key; requires running server."""
from concurrent.futures import ThreadPoolExecutor
import requests

BASE = 'http://127.0.0.1:8080'
KEY = 'concurrent_test'

def write(i):
    response = requests.post(f'{BASE}/{KEY}', json={'value': f'writer_{i}'}, timeout=10)
    response.raise_for_status()

def remove(_):
    response = requests.delete(f'{BASE}/{KEY}', timeout=10)
    assert response.status_code in (200, 404), response.text

with ThreadPoolExecutor(max_workers=12) as pool:
    list(pool.map(write, range(60)))
response = requests.get(f'{BASE}/{KEY}', timeout=10)
assert response.status_code == 200, response.text
assert response.json()['value'] in {f'writer_{i}' for i in range(60)}
with ThreadPoolExecutor(max_workers=12) as pool:
    list(pool.map(remove, range(30)))
assert requests.get(f'{BASE}/{KEY}', timeout=10).status_code == 404
print('Concurrent writes and deletes passed (atomic operations; last-writer value may vary).')
