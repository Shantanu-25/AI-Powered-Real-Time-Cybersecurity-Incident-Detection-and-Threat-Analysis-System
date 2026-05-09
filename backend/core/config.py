from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CyberSec AI MVP"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "soc_dashboard")

    # Alerts (SMTP)
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_TO: str = os.getenv("ALERT_EMAIL_TO", "")

    # Alerts (Telegram)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # ML Settings
    THREAT_SCORE_THRESHOLD: float = float(os.getenv("THREAT_SCORE_THRESHOLD", "0.75"))
    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml/random_forest_model.joblib")

    # Security
    CORS_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000", "*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
