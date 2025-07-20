from flask import Blueprint, render_template, request, jsonify
from flask_wtf import FlaskForm
from app.blueprints.passwords.services.generator import PasswordGenerator
from app.blueprints.passwords.services.analyzer import analyze_password
import logging
from app.extensions import csrf

logger = logging.getLogger(__name__)

# Creates a Blueprint for the main application routes.
# Organizes routes and templates under a common prefix.
main = Blueprint("main", __name__, template_folder="templates")

# Defines a simple FlaskForm for CSRF protection.
# Ensures all form submissions are secure against cross-site request forgery.
class CSRFProtectForm(FlaskForm):
    pass

@main.route("/", methods=["GET", "POST"])
def index():
    """
    Renders the main page and handles password generation and analysis requests.

    Handles GET requests to display the main page.
    Processes POST requests for either password generation based on user criteria
    or password analysis, including checking against pwned passwords.

    Returns:
        str: The rendered HTML of the main page, or a JSON response for AJAX requests.
    """
    password_result = None
    analysis = None
    logger.debug(f"Main blueprint - Incoming request method: {request.method}")
    if request.method == "POST":
        logger.debug(f"Main blueprint - Request form data: {request.form}")
        logger.debug(f"Main blueprint - Request headers: {request.headers}")

        # Determines if the request is an AJAX call.
        # Allows the server to respond appropriately with JSON or HTML.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                  request.headers.get('Content-Type') == 'application/json'

        # Handles password analysis requests.
        # Parses input passwords and performs security analysis.
        if "analyze" in request.form or (is_ajax and request.json and 'passwords' in request.json):
            passwords_data = request.form.get("passwords") if not is_ajax else request.json.get('passwords')
            check_pwned = request.form.get("check_pwned", type=bool, default=True) if not is_ajax else request.json.get('check_pwned', True)

            password_list = [p.strip() for p in passwords_data.split(",") if p.strip()]
            analysis_results = [analyze_password(p, check_pwned=check_pwned) for p in password_list]
            return jsonify(analysis_results=analysis_results)
        # Handles password generation requests.
        # Generates a new password based on user-specified criteria.
        else:
            try:
                # Parses generation options from either JSON (AJAX) or form data.
                # Ensures flexibility in handling different request types.
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

                # Prepares options for the password generator.
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

                # Returns generated password and analysis based on request type.
                if is_ajax:
                    return jsonify(password=result.get("password"), analysis=result.get("analysis"))
                else:
                    password_result = result.get("password")
                    analysis = result.get("analysis")

            # Handles errors during password generation.
            # Logs the error and returns an appropriate response.
            except ValueError as e:
                logger.error(f"Error during password generation: {e}")
                if is_ajax:
                    return jsonify({"error": str(e)}), 400
                else:
                    # In a real app, you'd flash this message to the user
                    pass

    # Initializes CSRF protection form and renders the main template.
    # Passes generated password and analysis results to the template for display.
    form = CSRFProtectForm()
    return render_template(
        "main/index.html", password_result=password_result, analysis=analysis, form=form
    )