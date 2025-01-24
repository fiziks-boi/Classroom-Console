#!/bin/bash

# Update package list and ensure Python and pip are installed
echo "Updating system packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found."
    exit 1
fi

# Make the script executable
chmod +x ai_script.py

echo "Setup complete! To run the program:"
echo "1. Activate the virtual environment with: source venv/bin/activate"
echo "2. Run the program with: python ai_script.py"
