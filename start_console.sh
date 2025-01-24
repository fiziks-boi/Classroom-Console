#!/bin/bash

# Navigate to the script's directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "$SCRIPT_DIR"

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run install.sh to set it up."
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run the script
echo "Starting AI CLI..."
python class_console_with_personas.py

# Deactivate the virtual environment when done
deactivate
