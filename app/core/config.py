import os

DEFAULT_SECRET_KEY = "dev-only-secret-key-change-me-in-production"

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./jobhub.db")
SECRET_KEY = os.environ.get("SECRET_KEY", DEFAULT_SECRET_KEY)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def check_settings() -> None:
    """Refuse to start in production with the development secret key."""
    if ENVIRONMENT == "production" and SECRET_KEY == DEFAULT_SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be set to a real secret when ENVIRONMENT=production")