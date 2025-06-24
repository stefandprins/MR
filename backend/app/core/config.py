import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "MR Recommender"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # FastAPI settings
    API_PREFIX: str = "/api"

    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

settings = Settings()