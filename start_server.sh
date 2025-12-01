#!/bin/bash

# Force UTF-8 encoding for the entire session
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Print encoding settings for verification
echo "PYTHONIOENCODING: $PYTHONIOENCODING"
echo "LANG: $LANG"
echo "LC_ALL: $LC_ALL"

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start uvicorn server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
