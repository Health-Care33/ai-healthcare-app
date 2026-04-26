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
    JWT_EXPIRATION: int = int(os.getenv("JWT_EXPIRATION", 1440))  # minutes

    # ---------- API KEYS ----------
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")

    # ---------- VALIDATION ----------
    def validate(self):
        if not self.MONGO_URI:
            print("⚠️ WARNING: MONGO_URI not set")

        if not self.GROQ_API_KEY:
            print("⚠️ WARNING: GROQ_API_KEY not set")

        if not self.OPENROUTER_API_KEY:
            print("⚠️ WARNING: OPENROUTER_API_KEY not set")


settings = Settings()
settings.validate()
