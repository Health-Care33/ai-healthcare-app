import os
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

from app.services.auth_service import register_user, login_user
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.database.mongodb import user_collection
from app.utils.security import SECRET_KEY, ALGORITHM

from authlib.integrations.starlette_client import OAuth


router = APIRouter()
security = HTTPBearer()

# GOOGLE OAUTH SETUP
oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


# REGISTER
@router.post("/register")
async def register(data: RegisterSchema):
    return await register_user(data)


# LOGIN
@router.post("/login")
async def login(data: LoginSchema):
    return await login_user(data)


# PROFILE
@router.get("/profile")
async def get_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please login again."
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    email = payload.get("email")

    user = await user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": user["name"],
        "email": user["email"]
    }


# GOOGLE LOGIN
@router.get("/google/login")
async def google_login(request: Request):

    redirect_uri = "https://ai-healthcare-backend-psnj.onrender.com/api/auth/google/callback"

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"
    )


# GOOGLE CALLBACK
@router.get("/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)

        # 🔥 FIX: userinfo safely fetch
        user = token.get("userinfo")

        if not user:
            resp = await oauth.google.get("userinfo", token=token)
            user = resp.json()

        if not user:
            raise HTTPException(status_code=400, detail="User info not found")

        email = user.get("email")
        name = user.get("name")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found")

        db_user = await user_collection.find_one({"email": email})

        if not db_user:
            await user_collection.insert_one({
                "name": name,
                "email": email,
                "created_at": datetime.utcnow()
            })

        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return RedirectResponse(
            f"https://ai-healthcare-app-6uqr-g6s51z6o5-health-care33s-projects.vercel.app/google-success?token={access_token}"
        )

    except Exception as e:
        print("GOOGLE CALLBACK ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))