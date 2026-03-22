import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    MONGO_URI: str = os.getenv("MONGO_URI")

    DATABASE_NAME: str = "ai_healthcare"

    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey123")

    JWT_ALGORITHM: str = "HS256"

    JWT_EXPIRATION: int = 60 * 24


settings = Settings()