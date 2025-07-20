from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

# Initializes CSRF protection.
# Prevents cross-site request forgery by validating form submissions.
csrf = CSRFProtect()
# Initializes the SQLAlchemy ORM.
# Manages database interactions using Python objects.
db = SQLAlchemy()