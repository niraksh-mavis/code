import os

class Config:
    DEBUG = True
    ENV = "development"
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portal.db")

    # Vulnerability: Hardcoded Secrets & API Keys (Low/Medium)
    SECRET_KEY = "dev-insecure-secret-key-change-in-production-12345"
    JWT_SECRET = "super-secret-jwt-token-998877665544332211"
    STRIPE_SECRET_KEY = "sk_live_51M0abcdef1234567890abcdef12345678"
    AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    # Insecure Session Cookie defaults (Low)
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = None
