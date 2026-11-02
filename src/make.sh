#!/usr/bin/env bash
# Full rebuild: builder engine -> images -> finishing pass.
set -euo pipefail
cd "$(dirname "$0")"
node build.js
python images.py
python finish.py
echo "--- build complete ---"
