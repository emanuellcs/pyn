from flask import Blueprint, request, render_template
import base64
import hashlib
import string
import random
import urllib.parse
import uuid
import json

tools = Blueprint("tools", __name__)


@tools.route("/", methods=["GET"])
def index():
    return render_template("tools/index.html")


@tools.route("/pin", methods=["POST"])
def generate_pin():
    length = int(request.form.get("length", 4))
    if not 4 <= length <= 12:
        return "Length must be between 4 and 12", 400
    pin = "".join(random.SystemRandom().choice(string.digits) for _ in range(length))
    return render_template("tools/partials/pin_result.html", pin=pin)


@tools.route("/encode", methods=["POST"])
def encode_string():
    action = request.form.get("action")  # 'encode' or 'decode'
    method = request.form.get("method")  # 'base64', 'hex', 'url'
    text = request.form.get("text", "")

    if not text:
        return ""

    result = ""
    try:
        if action == "encode":
            if method == "base64":
                result = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            elif method == "hex":
                result = text.encode("utf-8").hex()
            elif method == "url":
                result = urllib.parse.quote(text)
        elif action == "decode":
            if method == "base64":
                result = base64.b64decode(text.encode("utf-8")).decode("utf-8")
            elif method == "hex":
                result = bytes.fromhex(text).decode("utf-8")
            elif method == "url":
                result = urllib.parse.unquote(text)
    except Exception:
        result = "Error: Invalid input for decoding."

    return render_template("tools/partials/encode_result.html", result=result)


@tools.route("/hash", methods=["POST"])
def hash_string():
    text = request.form.get("text", "")
    if not text:
        return ""

    hashes = {
        "MD5 (Insecure)": hashlib.md5(text.encode()).hexdigest(),
        "SHA-1 (Insecure)": hashlib.sha1(text.encode()).hexdigest(),
        "SHA-256": hashlib.sha256(text.encode()).hexdigest(),
        "SHA-512": hashlib.sha512(text.encode()).hexdigest(),
    }

    return render_template("tools/partials/hash_result.html", hashes=hashes)


@tools.route("/uuid", methods=["POST"])
def generate_uuid():
    version = request.form.get("version", "4")
    count = int(request.form.get("count", 1))

    uuids = []
    for _ in range(min(count, 100)):  # Max 100 to prevent abuse
        if version == "1":
            uuids.append(str(uuid.uuid1()))
        else:
            uuids.append(str(uuid.uuid4()))

    return render_template("tools/partials/uuid_result.html", uuids=uuids)


@tools.route("/jwt", methods=["POST"])
def decode_jwt():
    token = request.form.get("token", "").strip()
    if not token:
        return ""

    parts = token.split(".")
    if len(parts) != 3:
        return render_template(
            "tools/partials/jwt_result.html",
            error="Invalid JWT format. Expected 3 parts.",
        )

    try:

        def decode_base64_url(s):
            s = s.replace("-", "+").replace("_", "/")
            padded = s + "=" * (4 - len(s) % 4)
            return base64.b64decode(padded).decode("utf-8")

        header = json.loads(decode_base64_url(parts[0]))
        payload = json.loads(decode_base64_url(parts[1]))

        return render_template(
            "tools/partials/jwt_result.html",
            header=json.dumps(header, indent=2),
            payload=json.dumps(payload, indent=2),
        )
    except Exception as e:
        return render_template(
            "tools/partials/jwt_result.html", error=f"Error decoding JWT: {str(e)}"
        )


@tools.route("/json", methods=["POST"])
def format_json():
    raw_json = request.form.get("json_input", "")
    if not raw_json.strip():
        return ""

    try:
        parsed = json.loads(raw_json)
        formatted = json.dumps(parsed, indent=4)
        return render_template(
            "tools/partials/json_result.html", formatted=formatted, success=True
        )
    except json.JSONDecodeError as e:
        return render_template(
            "tools/partials/json_result.html", error=str(e), success=False
        )
