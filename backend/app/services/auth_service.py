from fastapi import HTTPException
from app.database.mongodb import user_collection
from app.utils.security import hash_password, verify_password, create_access_token


async def register_user(data):

    email = data.email
    password = hash_password(data.password)

    existing_user = await user_collection.find_one({"email": email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = {
        "name": data.name,
        "email": email,
        "password": password
    }

    await user_collection.insert_one(user)

    return {"message": "User registered successfully"}


async def login_user(data):

    email = data.email
    password = data.password

    user = await user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    # ✅ FIXED TOKEN PAYLOAD
    token = create_access_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }