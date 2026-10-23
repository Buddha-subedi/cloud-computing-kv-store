"""Two-minute demo: run with server.py active in another terminal."""
import requests

BASE = 'http://127.0.0.1:8080'
KEY = 'demo_student'

def show(label, response):
    print(f'{label}: HTTP {response.status_code} {response.json()}')

if __name__ == '__main__':
    show('PUT', requests.post(f'{BASE}/{KEY}', json={'value': 'Buddha'}, timeout=5))
    show('GET', requests.get(f'{BASE}/{KEY}', timeout=5))
    show('UPDATE', requests.post(f'{BASE}/{KEY}', json={'value': 'Updated'}, timeout=5))
    show('GET updated', requests.get(f'{BASE}/{KEY}', timeout=5))
    show('DELETE', requests.delete(f'{BASE}/{KEY}', timeout=5))
    show('GET missing', requests.get(f'{BASE}/{KEY}', timeout=5))
