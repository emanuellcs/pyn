from flask import Blueprint, request, jsonify, render_template
from .services.analyzer import analyze_password, get_strength_from_score
from .services.generator import PasswordGenerator
from flask_wtf.csrf import validate_csrf, ValidationError
from app.extensions import db
from app.models.password_metrics import PasswordMetrics
import logging
import os
import csv

# Configures logging for the blueprint.
# Provides detailed debug information for requests and processes.
logger = logging.getLogger(__name__)

# Creates a Blueprint for password-related routes.
# Organizes password generation, analysis, and export functionalities.
passwords = Blueprint('passwords', __name__, template_folder='templates')

@passwords.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes multiple passwords provided in the request.

    Accepts a list of passwords and returns their security analysis,
    including strength and pwned status. Saves metrics to the database.
    """
    try:
        # Parses JSON request data.
        # Expects a 'passwords' field, optionally with 'check_pwned'.
        data = request.get_json()
        if not data or 'passwords' not in data:
            return jsonify({"error": "Missing 'passwords' in request body"}), 400
        
        passwords_data = data.get('passwords')
        check_pwned = data.get('check_pwned', True) # Default to True if not provided

        # Converts comma-separated string to a list of passwords if necessary.
        if isinstance(passwords_data, str):
            passwords_data = passwords_data.split(',')

        if not isinstance(passwords_data, list):
            return jsonify({"error": "'passwords' must be a list or a comma-separated string"}), 400

        results = []
        # Iterates through each password, performs analysis, and saves metrics.
        for password in passwords_data:
            raw_password = password.strip()
            if not raw_password:
                continue
            
            analysis_data = analyze_password(raw_password, check_pwned=check_pwned)
            # Adds strength based on zxcvbn score and saves to database.
            if analysis_data and 'zxcvbn_analysis' in analysis_data and 'score' in analysis_data['zxcvbn_analysis']:
                analysis_data['strength'] = get_strength_from_score(analysis_data['zxcvbn_analysis']['score'])
                
                # Saves password metrics to the database.
                # Stores entropy and score for historical analysis.
                new_metric = PasswordMetrics(
                    password=raw_password,
                    entropy=analysis_data['zxcvbn_analysis'].get('entropy', 0.0),
                    score=analysis_data['zxcvbn_analysis']['score']
                )
                db.session.add(new_metric)
                db.session.commit()

            results.append(analysis_data)

        # Returns the analysis results as a JSON response.
        return jsonify({"analysis_results": results})
    # Handles exceptions during password analysis.
    # Logs the error and returns a generic error message.
    except Exception as e:
        logger.error(f"Error during password analysis: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

@passwords.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the password generator page and handles password generation requests.

    Handles GET requests to display the password generation interface.
    Processes POST requests to generate a new password based on user-defined criteria.
    """
    if request.method == 'POST':
        try:
            # Parses password generation parameters from the JSON request body.
            data = request.get_json()
            length = int(data.get('length', 16))
            # Validates the requested password length.
            if not 8 <= length <= 64:
                logger.warning(f"Invalid password length received: {length}")
                return jsonify({"error": "Password length must be between 8 and 64."}), 400

            # Prepares options for the password generator.
            options = {
                'length': length,
                'use_upper': data.get('use_upper', False),
                'use_lower': data.get('use_lower', False),
                'use_digits': data.get('use_digits', False),
                'use_special': data.get('use_special', False),
                'exclude_chars': data.get('exclude_chars', '')
            }

            generator = PasswordGenerator()
            result = generator.generate(options)
            
            # Adds strength based on zxcvbn score to the analysis data.
            analysis_data = result.get('analysis')
            if analysis_data and 'zxcvbn_analysis' in analysis_data and 'score' in analysis_data['zxcvbn_analysis']:
                analysis_data['strength'] = get_strength_from_score(analysis_data['zxcvbn_analysis']['score'])
            
            # Returns the generated password and its analysis.
            return jsonify({
                "password_result": result.get('password'),
                "analysis": analysis_data
            })

        # Handles value errors during password generation.
        except ValueError as e:
            logger.error(f"Error generating password: {e}")
            return jsonify({"error": str(e)}), 400
        # Handles other internal server errors during password generation.
        except Exception as e:
            logger.error(f"An internal server error occurred during password generation: {e}")
            return jsonify({"error": "An internal server error occurred."}), 500

    # Renders the password generator HTML page for GET requests.
    return render_template('passwords/index.html')

@passwords.route('/export', methods=['POST'])
def export():
    """
    Exports password analysis results to a file.

    Accepts a list of passwords and a desired file format (e.g., CSV),
    then generates a file containing the analysis results.
    """
    passwords_data = request.form.get('passwords', '').split(',')
    file_format = request.form.get('format', 'csv')
    filename = f"password_analysis.{file_format}"

    results = []
    # Analyzes each password for export.
    for password in passwords_data:
        password = password.strip()
        results.append(analyze_password(password))

    # Handles CSV export format.
    if file_format == 'csv':
        # Defines the export directory and creates it if it doesn't exist.
        # Note: In a production environment, this should be handled more securely
        # to prevent path traversal vulnerabilities and ensure proper file storage.
        export_dir = os.path.join(os.getcwd(), 'exports')
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, filename)

        # Writes analysis results to a CSV file.
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        # Returns a success message with the export file path.
        return jsonify({"message": "Exported successfully", "filepath": filepath})

    # Returns an error for unsupported file formats.
    return jsonify({"error": "Unsupported format"}), 400