import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # ---------- DATABASE ----------
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ai_healthcare")

    # ---------- JWT ----------
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey123")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION: int = 60 * 24

    # ---------- API KEYS ----------
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")


settings = Settings()