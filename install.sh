#!/bin/sh
set -eu

MIN_PYTHON="3.9"
PYTHON=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 9))'; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Python $MIN_PYTHON or newer is required. Install it from https://www.python.org/downloads/ and run this script again." >&2
    exit 1
fi

VERSION=$("$PYTHON" -c 'import platform; print(platform.python_version())')
echo "Using Python $VERSION ($PYTHON)"
"$PYTHON" -m venv .venv
".venv/bin/python" -m pip install --upgrade pip
".venv/bin/python" -m pip install .
echo ""
echo "Installation complete. Run:"
echo "  .venv/bin/echo360-transcripts --help"
echo "  .venv/bin/echo360-transcripts COURSE_URL --output ./transcripts --zip"
