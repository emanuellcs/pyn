#!/bin/bash

echo "Setting up the Pyn application..."

echo "Creating virtual environment and installing dependencies..."
bash scripts/setup_linux.sh # Assuming setup_linux.sh also works for macOS

echo "Activating virtual environment..."
source venv/bin/activate

echo "Initializing the database..."
flask init-db

echo "Running the application..."
python run.py

echo "Setup complete. The application should now be running."