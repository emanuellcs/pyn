#!/bin/bash
echo "Setting up the Pyn application..."

# Change directory to the project root (parent directory of scripts)
cd ..

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setting FLASK_APP environment variable..."
export FLASK_APP=run.py

echo "Initializing the database..."
flask init-db

echo "Running the application..."
python3 run.py

echo "Setup complete. The application should now be running."
