#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")" || { echo "Failed to change directory"; exit 1; }

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
  # Create virtual environment
  echo "Creating virtual environment..."
  python3 -m venv venv
  if [ $? -eq 0 ]; then
    echo "Virtual environment created."
  else
    echo "Failed to create virtual environment."
    exit 1
  fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
  echo "Virtual environment activated."
else
  echo "Failed to activate virtual environment."
  exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
  echo "Dependencies installed."
else
  echo "Failed to install dependencies."
  exit 1
fi

# Run the Streamlit application
echo "Running Streamlit application..."
streamlit run src/Home.py
