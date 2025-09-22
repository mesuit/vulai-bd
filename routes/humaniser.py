from flask import Blueprint, request, jsonify, current_app
import requests

humaniser_bp = Blueprint("humaniser", __name__)

@humaniser_bp.route("/humaniser", methods=["POST"])
def humanise_text():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        api_key = current_app.config["HUMANISE_API_KEY"]
        url = "https://www.humanizeai.pro/api/humanize"

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"text": text}

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        return jsonify({"original": text, "humanised": result.get("humanized_text")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
