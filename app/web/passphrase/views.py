from flask import Blueprint, request, render_template, jsonify, current_app
import logging
import os
from app.core.application.passphrase_service import PassphraseApplicationService
from app.extensions import db
from app.infrastructure.persistence.password_metrics import PasswordMetrics

logger = logging.getLogger(__name__)
passphrase = Blueprint("passphrase", __name__)


@passphrase.route("/", methods=["GET"])
def index():
    return render_template("passphrase/index.html")


@passphrase.route("/generate", methods=["POST"])
def generate():
    """HTMX endpoint for generating a passphrase."""
    try:
        num_words = int(request.form.get("num_words", 4))
        if not 3 <= num_words <= 20:
            return "Number of words must be between 3 and 20.", 400

        separator = request.form.get("separator", "-")
        generator_type = request.form.get("generator_type", "diceware")

        # Wordlist path in the new infrastructure resources location
        wordlist_path = os.path.join(
            current_app.root_path,
            "infrastructure",
            "resources",
            "eff_large_wordlist.txt",
        )

        result = PassphraseApplicationService.generate(
            num_words, generator_type, separator, wordlist_path
        )
        passphrase_str = result["passphrase"]
        analysis = result["analysis"]

        metric = PasswordMetrics(
            password=passphrase_str,
            entropy=analysis["password_strength_metrics"]["entropy"],
            score=analysis["zxcvbn_analysis"]["score"],
        )
        db.session.add(metric)
        db.session.commit()

        if request.headers.get("HX-Request"):
            return render_template(
                "passwords/partials/result.html",
                password=passphrase_str,
                analysis=analysis,
            )

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error generating passphrase: {e}")
        return "Internal error", 500
