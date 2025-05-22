#!/bin/bash
# Setup script for the Serial Log Testing Platform virtual environment

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [ -d "venv/bin" ]; then
    source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
    # Windows environment
    source venv/Scripts/activate
else
    echo "Failed to find activation script. Virtual environment may not have been created correctly."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

echo "Setup complete. Activate the virtual environment with:"
echo "  - On Linux/Mac: source venv/bin/activate"
echo "  - On Windows: venv\\Scripts\\activate" 