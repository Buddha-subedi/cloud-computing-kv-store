#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python demo.py
python test_server.py
python test_concurrency.py
python kv_bench.py
