from flask import Blueprint, request, jsonify
import requests

humaniser_bp = Blueprint("humaniser", __name__)

@humaniser_bp.route("/humanise", methods=["POST"])
def humanise():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Simulate a browser request to humanizeai.pro
        url = "https://www.humanizeai.pro/"  # adjust if you want a specific endpoint
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        response = requests.post(url, headers=headers, data={"text": text}, timeout=30)

        if response.status_code == 200:
            return jsonify({"success": True, "output": response.text})
        else:
            return jsonify({
                "success": False,
                "status_code": response.status_code,
                "error": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
