from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config.settings import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ✅ SAFE SECRET FIX
SECRET_KEY = settings.JWT_SECRET or "ai_healthcare_super_secret_key"

ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = 2


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token