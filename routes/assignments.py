from flask import Blueprint, jsonify

assignments_bp = Blueprint("assignments", __name__)

categories = [
    {"id": 1, "name": "Essays"},
    {"id": 2, "name": "Reports"},
    {"id": 3, "name": "Case Studies"}
]

@assignments_bp.route("/", methods=["GET"])
def get_categories():
    return jsonify(categories)
