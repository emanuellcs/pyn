from flask import Blueprint, jsonify, render_template, request
from flask_wtf import FlaskForm
from .services.generator import PassphraseGenerator
from .services.analyzer import analyze_passphrase
from flask_wtf.csrf import validate_csrf, ValidationError
import logging

# Configures logging for the blueprint.
# Provides detailed debug information for requests and processes.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Creates a Blueprint for passphrase-related routes.
# Organizes passphrase generation and analysis functionalities.
passphrase = Blueprint('passphrase', __name__, template_folder='templates')

# Defines a simple FlaskForm for CSRF protection.
# Ensures all form submissions are secure against cross-site request forgery.
class CSRFProtectForm(FlaskForm):
    pass

@passphrase.route('/', methods=['GET'])
def index():
    """
    Renders the passphrase generation page.
    Displays the main interface for users to generate and analyze passphrases.
    """
    form = CSRFProtectForm()
    return render_template('passphrase/index.html', form=form)

@passphrase.route('/generate', methods=['POST'])
def generate():
    """
    Generates a passphrase based on user-provided criteria.
    Handles AJAX POST requests, validates CSRF token, and returns a JSON response
    containing the generated passphrase and its security analysis.
    """
    # Logs incoming request headers for debugging.
    logger.debug(f"Incoming headers: {request.headers}")
    csrf_token_header = request.headers.get('X-CSRFToken')
    logger.debug(f"X-CSRFToken header: {csrf_token_header}")

    # Manually validates the CSRF token for JSON endpoints.
    # Protects against cross-site request forgery attacks.
    try:
        validate_csrf(csrf_token_header)
        logger.debug("CSRF token validated successfully.")
    except ValidationError as e:
        logger.error(f"CSRF validation failed: {e}")
        return jsonify({'error': 'CSRF token missing or invalid.'}), 403

    # Extracts passphrase generation parameters from the JSON request body.
    data = request.get_json()
    num_words = data.get('num_words', 4)
    separator = data.get('separator', '-')
    capitalize = data.get('capitalize', False)

    try:
        # Instantiates the PassphraseGenerator and generates a passphrase.
        # Uses the EFF large wordlist for strong, memorable passphrases.
        logger.debug(f"Attempting to instantiate PassphraseGenerator with wordlist_path: app/blueprints/passphrase/services/eff_large_wordlist.txt")
        generator = PassphraseGenerator("app/blueprints/passphrase/services/eff_large_wordlist.txt")
        passphrase_text = generator.generate(
            num_words=num_words,
            separator=separator,
            capitalize=capitalize
        )
        # Analyzes the generated passphrase for security metrics.
        analysis = analyze_passphrase(passphrase_text)
        return jsonify({
            'passphrase': passphrase_text,
            'analysis': analysis
        })
    # Handles errors during passphrase generation.
    # Returns an error message to the client.
    except (ValueError, TypeError) as e:
        logger.error(f"Error generating passphrase: {e}")
        return jsonify({'error': str(e)}), 400