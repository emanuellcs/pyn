from flask import Blueprint, render_template, request, jsonify
from flask_wtf import FlaskForm
from app.blueprints.passwords.services.generator import PasswordGenerator
from app.blueprints.passwords.services.analyzer import analyze_password
import logging
from app.extensions import csrf # Import csrf from extensions

# Configure logging
logger = logging.getLogger(__name__)

main = Blueprint("main", __name__, template_folder="templates")

# Exempt the passphrase.generate route from automatic CSRF protection
# as it's now manually validated.
# This line should be placed after the blueprint is defined.
# @csrf.exempt
# @passphrase.route('/generate', methods=['POST']) # This is in passphrase blueprint, not main.

class CSRFProtectForm(FlaskForm):
    pass

@main.route("/", methods=["GET", "POST"])
def index():
    """
    Renders the main page and handles password generation requests.

    On GET, it serves the main entry point of the application.
    On POST, it handles the password generation form submission,
    creating a new password based on user-defined criteria.

    Returns:
        str: The rendered HTML of the main page, optionally with the
             generated password and its analysis.
    """
    password_result = None
    analysis = None
    logger.debug(f"Main blueprint - Incoming request method: {request.method}")
    if request.method == "POST":
        logger.debug(f"Main blueprint - Request form data: {request.form}")
        logger.debug(f"Main blueprint - Request headers: {request.headers}")

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                  request.headers.get('Content-Type') == 'application/json'

        # Handle password analysis request
        if "analyze" in request.form or (is_ajax and request.json and 'passwords' in request.json):
            passwords_data = request.form.get("passwords") if not is_ajax else request.json.get('passwords')
            check_pwned = request.form.get("check_pwned", type=bool, default=True) if not is_ajax else request.json.get('check_pwned', True)

            password_list = [p.strip() for p in passwords_data.split(",") if p.strip()]
            analysis_results = [analyze_password(p, check_pwned=check_pwned) for p in password_list]
            return jsonify(analysis_results=analysis_results)
        # Handle password generation request
        else: # Handle password generation request
            try:
                if is_ajax:
                    length = request.json.get("length", 16)
                    use_upper = request.json.get("use_upper", True)
                    use_lower = request.json.get("use_lower", True)
                    use_digits = request.json.get("use_digits", True)
                    use_special = request.json.get("use_special", True)
                    exclude_chars = request.json.get("exclude_chars", "")
                else:
                    length = request.form.get("length", default=16, type=int)
                    use_upper = request.form.get("use_upper") == "on"
                    use_lower = request.form.get("use_lower") == "on"
                    use_digits = request.form.get("use_digits") == "on"
                    use_special = request.form.get("use_special") == "on"
                    exclude_chars = request.form.get("exclude_chars", "")

                options = {
                    "length": int(length),
                    "use_upper": bool(use_upper),
                    "use_lower": bool(use_lower),
                    "use_digits": bool(use_digits),
                    "use_special": bool(use_special),
                    "exclude_chars": exclude_chars,
                }

                generator = PasswordGenerator()
                result = generator.generate(options)

                if is_ajax:
                    return jsonify(password=result.get("password"), analysis=result.get("analysis"))
                else:
                    password_result = result.get("password")
                    analysis = result.get("analysis")

            except ValueError as e:
                logger.error(f"Error during password generation: {e}")
                if is_ajax:
                    return jsonify({"error": str(e)}), 400
                else:
                    # In a real app, you'd flash this message to the user
                    pass

    form = CSRFProtectForm()
    return render_template(
        "main/index.html", password_result=password_result, analysis=analysis, form=form
    )