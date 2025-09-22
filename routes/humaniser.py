from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

humaniser_bp = Blueprint("humaniser", __name__)

@humaniser_bp.route("/humanise", methods=["POST"])
def humanise():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        url = "https://www.humanizeai.pro/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        # Send the request (adjust data field name if site expects different one)
        response = requests.post(url, headers=headers, data={"text": text}, timeout=30)

        if response.status_code != 200:
            return jsonify({
                "success": False,
                "status_code": response.status_code,
                "error": response.text[:200]  # preview only
            }), response.status_code

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # You’ll need to inspect the site’s HTML to find the correct element.
        # For example, assume humanised text appears in <div class="result-text">
        result_div = soup.find("div", class_="result-text")

        if result_div:
            humanised_text = result_div.get_text(strip=True)
        else:
            humanised_text = None

        return jsonify({
            "success": True,
            "output": humanised_text or "Could not extract humanised text"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
