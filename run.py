# Imports necessary modules for application creation and database management.
from app import create_app, db
from app.models.password_metrics import PasswordMetrics

# Initializes the Flask application, configuring it based on the environment.
app = create_app()

# Registers a command-line interface (CLI) command to set up the database.
@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    # Ensures the database tables are created within the application context.
    with app.app_context():
        db.create_all()
    # Informs the user that the database has been successfully initialized.
    print('Initialized the database.')

# Checks if the script is being run directly to start the development server.
if __name__ == '__main__':
    # Runs the Flask application in debug mode for development purposes.
    app.run(debug=True)