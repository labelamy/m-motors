#!/bin/bash

set -e
echo "Starting server..."

python --version
pwd
ls

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}