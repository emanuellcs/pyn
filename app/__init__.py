from flask import Flask
from .extensions import csrf, db


# Initializes and configures the Flask application.
# Sets up the application context based on the specified environment.
def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")

    # Initializes Flask extensions.
    # Integrates services like CSRF protection and database for application-wide use.
    csrf.init_app(app)
    db.init_app(app)

    # Registers blueprints.
    # Organizes routes and views into modular components for better application structure.
    from .web.main.views import main
    from .web.passwords.views import passwords
    from .web.passphrase.views import passphrase
    from .web.tools.views import tools
    from .web.dashboard.views import dashboard

    app.register_blueprint(main)
    app.register_blueprint(passwords, url_prefix="/passwords")
    app.register_blueprint(passphrase, url_prefix="/passphrase")
    app.register_blueprint(tools, url_prefix="/tools")
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    with app.app_context():
        db.create_all()

    # Returns the Flask application instance.
    # Provides the configured application ready for deployment.
    return app
