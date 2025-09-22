from flask import Blueprint, request, jsonify, current_app
import stripe

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout():
    data = request.json
    amount = data.get("amount", 500)  # default 5 USD

    try:
        stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Assignment Service"},
                    "unit_amount": amount * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:3000/payment-success",
            cancel_url="http://localhost:3000/payment-cancel",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
