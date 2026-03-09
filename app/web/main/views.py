from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    """
    Renders the main landing page.
    """
    return render_template("main/index.html")
