# Main application entry point for the password analysis web service.
# This file sets up the Flask application and configures routing.

from flask import Flask
from routes import setup_routes

# Initialize the Flask application
app = Flask(__name__)

# Configure all routes from routes.py
setup_routes(app)

# Run the application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)

# Define default headers for API responses
tempHeader = {'Content-Type': 'application/json'}  # Default header for JSON responses
