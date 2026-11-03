#!/usr/bin/env bash
# Full rebuild: merge content parts -> image pipeline -> render the site.
# render.py is the active builder; it emits pages in the original
# plinthrenovations.co.za markup and ships that site's styles.css and script.js.
set -euo pipefail
cd "$(dirname "$0")"
node build.js      # merges content-part*.json into content.json and generates pages
python images.py   # writes src/_images from the owner's photographs
python render.py   # clears site-output and rebuilds all pages in the original design
echo "--- build complete ---"
