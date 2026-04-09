#!/bin/bash

set -e

echo "Starting Amazing AI Spele..."

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in your PATH."
    echo "Please install Python 3.10+ (e.g. sudo pacman -S python)."
    read -p "Press Enter to exit..."
    exit 1
fi

# Prefer python3 if available, else python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating a portable virtual environment..."
    $PYTHON_CMD -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies silently
echo "Installing and verifying dependencies..."
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

# Run the Streamlit application
echo "Launching the game UI..."
export PYTHONPATH="$(pwd)"
streamlit run src/ui/app.py
