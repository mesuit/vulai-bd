from flask import Blueprint, request, jsonify
from playwright.sync_api import sync_playwright

humaniser_bp = Blueprint("humaniser", __name__)

@humaniser_bp.route("/humaniser", methods=["POST"])
def humanise_text():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Go to the site
            page.goto("https://www.humanizeai.pro/")

            # Type into the input area (update selector if different)
            page.fill("textarea", text)

            # Click the "Humanize" button (update selector if different)
            page.click("button:has-text('Humanize')")

            # Wait for result (adjust selector depending on site output)
            page.wait_for_selector(".result-output")

            # Extract processed text
            result = page.inner_text(".result-output")

            browser.close()

        return jsonify({"original": text, "humanised": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
