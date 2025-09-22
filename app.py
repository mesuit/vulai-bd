from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)

    from routes.auth import auth_bp
    from routes.humaniser import humaniser_bp
    from routes.assignments import assignments_bp
    from routes.payments import payments_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(humaniser_bp, url_prefix="/api/tools")
    app.register_blueprint(assignments_bp, url_prefix="/api/assignments")
    app.register_blueprint(payments_bp, url_prefix="/api/payment")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
