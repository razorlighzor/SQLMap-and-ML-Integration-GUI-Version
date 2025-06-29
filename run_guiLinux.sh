#!/bin/bash

# Activate your Python environment if you have one
# source venv/bin/activate

echo "Starting SQLMap-and-ML-Integration-GUI-Version..."

# Move to GUI directory
cd "$(dirname "$0")/GUI" || exit 1

# Run the main GUI script
python3 SQLiGUI.py

