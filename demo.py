"""Demonstrate logical GET, PUT, DEL operations using standard HTTP methods."""
import requests

BASE = "http://127.0.0.1:8080/demo_student"

def show(label, response):
    print(f"{label}: HTTP {response.status_code} {response.json()}")

if __name__ == "__main__":
    show("PUT", requests.put(BASE, json={"value": "first_value"}, timeout=10))
    show("GET", requests.get(BASE, timeout=10))
    show("PUT update", requests.put(BASE, json={"value": "updated_value"}, timeout=10))
    show("GET updated", requests.get(BASE, timeout=10))
    show("DEL", requests.delete(BASE, timeout=10))
    show("GET missing", requests.get(BASE, timeout=10))
