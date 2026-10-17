import os

# Read from environment variables. The defaults are for local development only.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./jobhub.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))