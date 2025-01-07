# This file contains all the routes for handling password analysis and generation requests.
from flask import Flask, request, render_template, jsonify
from password_analyzer import PasswordAnalysis
from password_generator import PasswordGenerator
import os
import csv

def setup_routes(app):
    """Configure all routes for the Flask application"""
    
    # Initialize password generator
    generator = PasswordGenerator()
    
    @app.route('/')
    def index():
        """Serve the main application page"""
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        """Analyze multiple passwords provided in the request"""
        passwords = request.form.get('passwords', '').split(',')
        results = []

        for password in passwords:
            raw_password = password.strip()
            analyzer = PasswordAnalysis(raw_password)
            analyzer.analyze()
            results.append(analyzer.report())

        return jsonify(results)

    @app.route('/generate', methods=['POST'])
    def generate():
        """Generate a password based on provided criteria"""
        try:
            options = request.get_json()
            if not options:
                raise ValueError("No options provided")

            length = options.get('length')
            if length is not None and int(length) > 64:
                return jsonify({"error": "Password length should not be greater than 64."}), 400

            result = generator.generate(options)
            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/export', methods=['POST'])
    def export():
        """Export password analysis results to a file"""
        passwords = request.form.get('passwords', '').split(',')
        file_format = request.form.get('format', 'csv')
        filename = f"password_analysis.{file_format}"

        results = []
        for password in passwords:
            password = password.strip()
            analyzer = PasswordAnalysis(password)
            analyzer.analyze()
            results.append(analyzer.report())

        if file_format == 'csv':
            filepath = os.path.join('exports', filename)
            os.makedirs('exports', exist_ok=True)

            with open(filepath, 'w', newline='') as csvfile:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    writer.writerow(result)

            return jsonify({"message": "Exported successfully", "filepath": filepath})

        return jsonify({"error": "Unsupported format"}), 400
