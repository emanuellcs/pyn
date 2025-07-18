from flask import Flask
from .extensions import csrf

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f'app.config.{config_name}')

    # Initialize extensions
    csrf.init_app(app)

    # Register blueprints
    from .blueprints.main.routes import main
    from .blueprints.passwords.routes import passwords
    from .blueprints.passphrase.routes import passphrase

    app.register_blueprint(main)
    app.register_blueprint(passwords, url_prefix='/passwords')
    app.register_blueprint(passphrase, url_prefix='/passphrase')

    return app