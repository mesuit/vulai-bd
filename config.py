import os
from dotenv import load_dotenv

# Load environment variables from .env (local dev only)
load_dotenv()

class Config:
    # Security key
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")

    # Database: prefer Render's DATABASE_URL (Postgres), fallback to SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///instance/app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Stripe
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

    # Bcrypt rounds (optional, security tuning)
    BCRYPT_LOG_ROUNDS = int(os.getenv("BCRYPT_LOG_ROUNDS", 12))

