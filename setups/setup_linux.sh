# setup.sh (Linux)
#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate