#!/bin/bash

# run_appimager.sh
# -----------------
# This script ensures a Python virtual environment exists in ./venv,
# creates it if missing, activates it, and runs run_app.py.
# Usage: ./run_appimager.sh
# Steps:
#   1. Checks for ./venv directory.
#   2. Creates venv if not found.
#   3. Activates the virtual environment.
#   4. Runs run_app.py with Python.

VENV_PATH="venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Creating at $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"
echo "Virtual environment activated."

python3 run_app.py