from flask import Blueprint, request, jsonify, render_template
from .services.analyzer import analyze_password, get_strength_from_score
from .services.generator import PasswordGenerator
from flask_wtf.csrf import validate_csrf, ValidationError
import logging
import os
import csv

# Configure logging
logger = logging.getLogger(__name__)

passwords = Blueprint('passwords', __name__, template_folder='templates')

@passwords.route('/analyze', methods=['POST'])
def analyze():
    """Analyze multiple passwords provided in the request"""
    try:
        data = request.get_json()
        if not data or 'passwords' not in data:
            return jsonify({"error": "Missing 'passwords' in request body"}), 400
        
        passwords_data = data.get('passwords')
        check_pwned = data.get('check_pwned', True) # Default to True if not provided

        if isinstance(passwords_data, str):
            passwords_data = passwords_data.split(',')

        if not isinstance(passwords_data, list):
            return jsonify({"error": "'passwords' must be a list or a comma-separated string"}), 400

        results = []
        for password in passwords_data:
            raw_password = password.strip()
            if not raw_password:
                continue
            results.append(analyze_password(raw_password, check_pwned=check_pwned))

        return jsonify({"analysis_results": results})
    except Exception as e:
        logger.error(f"Error during password analysis: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

@passwords.route('/', methods=['GET', 'POST'])
def index():
    """Render the password generator page and handle password generation."""
    if request.method == 'POST':
        try:
            data = request.get_json()
            length = int(data.get('length', 16))
            if not 8 <= length <= 64:
                logger.warning(f"Invalid password length received: {length}")
                return jsonify({"error": "Password length must be between 8 and 64."}), 400

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
            
            analysis_data = result.get('analysis')
            if analysis_data and 'zxcvbn_analysis' in analysis_data and 'score' in analysis_data['zxcvbn_analysis']:
                analysis_data['strength'] = get_strength_from_score(analysis_data['zxcvbn_analysis']['score'])
            
            return jsonify({
                "password_result": result.get('password'),
                "analysis": analysis_data
            })

        except ValueError as e:
            logger.error(f"Error generating password: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"An internal server error occurred during password generation: {e}")
            return jsonify({"error": "An internal server error occurred."}), 500

    return render_template('passwords/index.html')

@passwords.route('/export', methods=['POST'])
def export():
    """Export password analysis results to a file"""
    passwords_data = request.form.get('passwords', '').split(',')
    file_format = request.form.get('format', 'csv')
    filename = f"password_analysis.{file_format}"

    results = []
    for password in passwords_data:
        password = password.strip()
        results.append(analyze_password(password))

    if file_format == 'csv':
        # This should be handled more robustly in a real application
        # to avoid path issues and security risks.
        export_dir = os.path.join(os.getcwd(), 'exports')
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, filename)

        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        return jsonify({"message": "Exported successfully", "filepath": filepath})

    return jsonify({"error": "Unsupported format"}), 400