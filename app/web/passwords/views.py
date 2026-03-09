from flask import Blueprint, request, render_template, jsonify
import csv
import io
import logging
from app.core.application.password_service import PasswordApplicationService
from app.infrastructure.crypto import CryptoService
from app.extensions import db
from app.infrastructure.persistence.password_metrics import PasswordMetrics
from app.core.domain.password import PasswordGenerator

logger = logging.getLogger(__name__)
passwords = Blueprint("passwords", __name__)


@passwords.route("/", methods=["GET"])
def index():
    return render_template("passwords/index.html")


@passwords.route("/generate", methods=["POST"])
def generate():
    """HTMX endpoint for generating a password and analyzing it."""
    try:
        length = int(request.form.get("length", 16))

        # Explicitly check for checkbox presence and ensure boolean values
        generator = PasswordGenerator()
        result = generator.generate(
            length=length,
            use_upper="use_upper" in request.form,
            use_lower="use_lower" in request.form,
            use_digits="use_digits" in request.form,
            use_special="use_special" in request.form,
        )
        password = result.get("password")

        analysis = PasswordApplicationService.analyze(password)

        # Save to DB
        metric = PasswordMetrics(
            password=password,
            entropy=analysis["password_strength_metrics"]["entropy"],
            score=analysis["zxcvbn_analysis"]["score"],
        )
        db.session.add(metric)
        db.session.commit()

        if request.headers.get("HX-Request"):
            return render_template(
                "passwords/partials/result.html", password=password, analysis=analysis
            )
        return jsonify({"password": password, "analysis": analysis})
    except Exception as e:
        logger.error(f"Error generating: {e}")
        return "Error generating password", 500


@passwords.route("/analyze_input", methods=["POST"])
def analyze_input():
    """HTMX endpoint for real-time password analysis."""
    password = request.form.get("password", "")
    if not password:
        return ""

    analysis = PasswordApplicationService.analyze(password)
    return render_template(
        "passwords/partials/analysis_details.html", analysis=analysis
    )


@passwords.route("/hashes", methods=["POST"])
def get_hashes():
    """Developer Utility: get hashes for a given password."""
    password = request.form.get("password", "")
    if not password:
        return ""

    argon2_hash = CryptoService.hash_argon2(password)
    bcrypt_hash = CryptoService.hash_bcrypt(password)

    return render_template(
        "passwords/partials/hashes.html", argon2=argon2_hash, bcrypt=bcrypt_hash
    )


@passwords.route("/bulk_analyze", methods=["POST"])
def bulk_analyze():
    """Bulk CSV offline analysis."""
    if "csv_file" not in request.files:
        return "No file uploaded", 400

    file = request.files["csv_file"]
    if file.filename == "":
        return "No selected file", 400

    if file and file.filename.endswith(".csv"):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        results = []
        for row in csv_input:
            if not row:
                continue
            pwd = row[0].strip()
            if pwd:
                analysis = PasswordApplicationService.analyze(pwd, check_pwned=False)
                results.append(
                    {
                        "password": pwd,
                        "strength": analysis["strength"],
                        "score": analysis["zxcvbn_analysis"]["score"],
                    }
                )

        return render_template("passwords/partials/bulk_results.html", results=results)

    return "Invalid file type", 400
