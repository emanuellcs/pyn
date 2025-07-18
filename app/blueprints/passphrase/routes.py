from flask import Blueprint, jsonify, render_template, request
from flask_wtf import FlaskForm
from .services.generator import PassphraseGenerator
from .services.analyzer import analyze_passphrase
from flask_wtf.csrf import validate_csrf, ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

passphrase = Blueprint('passphrase', __name__, template_folder='templates')

class CSRFProtectForm(FlaskForm):
    pass


@passphrase.route('/', methods=['GET'])
def index():
    form = CSRFProtectForm()
    return render_template('passphrase/index.html', form=form)

@passphrase.route('/generate', methods=['POST'])
def generate():
    # Log the incoming request headers for debugging
    logger.debug(f"Incoming headers: {request.headers}")
    csrf_token_header = request.headers.get('X-CSRFToken')
    logger.debug(f"X-CSRFToken header: {csrf_token_header}")

    # Manual CSRF validation for JSON endpoint
    try:
        validate_csrf(csrf_token_header)
        logger.debug("CSRF token validated successfully.")
    except ValidationError as e:
        logger.error(f"CSRF validation failed: {e}")
        return jsonify({'error': 'CSRF token missing or invalid.'}), 403

    data = request.get_json()
    num_words = data.get('num_words', 4)
    separator = data.get('separator', '-')
    capitalize = data.get('capitalize', False)

    try:
        logger.debug(f"Attempting to instantiate PassphraseGenerator with wordlist_path: app/blueprints/passphrase/services/eff_large_wordlist.txt")
        generator = PassphraseGenerator("app/blueprints/passphrase/services/eff_large_wordlist.txt")
        passphrase_text = generator.generate(
            num_words=num_words,
            separator=separator,
            capitalize=capitalize
        )
        analysis = analyze_passphrase(passphrase_text)
        return jsonify({
            'passphrase': passphrase_text,
            'analysis': analysis
        })
    except (ValueError, TypeError) as e:
        logger.error(f"Error generating passphrase: {e}")
        return jsonify({'error': str(e)}), 400