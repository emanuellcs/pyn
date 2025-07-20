# Enables debug mode for the application.
# This provides detailed error messages and reloads the server on code changes.
DEBUG = True

# Sets a secret key for cryptographic operations.
# This protects against cross-site request forgery (CSRF) and other security vulnerabilities.
SECRET_KEY = "dev-key"

# Configures the database URI for SQLAlchemy.
# This specifies the connection string for the SQLite database used in development.
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'