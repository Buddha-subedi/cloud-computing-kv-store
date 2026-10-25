"""Single-process HTTP key-value store with SQLite persistence."""
import logging
import os
import sqlite3
import threading
from contextlib import contextmanager
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = os.environ.get("KV_DB", "kv_store.db")
HOST = os.environ.get("KV_HOST", "127.0.0.1")
PORT = int(os.environ.get("KV_PORT", "8080"))
write_lock = threading.Lock()
logging.basicConfig(filename="kv_operations.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

@contextmanager
def database():
    """Open, commit/rollback, and close a connection for each operation."""
    db = sqlite3.connect(DB_PATH, timeout=30)
    try:
        db.execute("PRAGMA busy_timeout=30000")
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def initialize():
    with database() as db:
        db.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT NOT NULL)")

@app.route("/<key>", methods=["PUT", "POST"])
def put(key):
    """PUT creates/replaces a value; POST is an instructor-benchmark compatibility alias."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("value"), str):
        logging.warning("PUT key=%r method=%s status=400", key, request.method)
        return jsonify(error="Expected JSON object with string field 'value'"), 400
    try:
        with write_lock:
            with database() as db:
                db.execute("INSERT INTO kv(key,value) VALUES(?,?) "
                           "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                           (key, data["value"]))
        logging.info("PUT key=%r method=%s status=200", key, request.method)
        return jsonify(key=key, value=data["value"]), 200
    except sqlite3.Error:
        logging.exception("PUT key=%r status=500", key)
        return jsonify(error="Database error"), 500

@app.route("/<key>", methods=["GET"])
def get(key):
    try:
        with database() as db:
            row = db.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
        if row is None:
            logging.info("GET key=%r status=404", key)
            return jsonify(error="Key not found"), 404
        logging.info("GET key=%r status=200", key)
        return jsonify(key=key, value=row[0]), 200
    except sqlite3.Error:
        logging.exception("GET key=%r status=500", key)
        return jsonify(error="Database error"), 500

@app.route("/<key>", methods=["DELETE"])
def delete(key):
    try:
        with write_lock:
            with database() as db:
                deleted = db.execute("DELETE FROM kv WHERE key=?", (key,)).rowcount
        status = 200 if deleted else 404
        logging.info("DEL key=%r status=%s", key, status)
        if deleted:
            return jsonify(message="Deleted", key=key), 200
        return jsonify(error="Key not found"), 404
    except sqlite3.Error:
        logging.exception("DEL key=%r status=500", key)
        return jsonify(error="Database error"), 500

if __name__ == "__main__":
    initialize()
    app.run(host=HOST, port=PORT, threaded=True, debug=False, use_reloader=False)
