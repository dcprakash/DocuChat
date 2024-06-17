#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
  # Create virtual environment
  python3 -m venv venv
  echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run src/pages/Home.py

# Deactivate virtual environment after use
deactivate
