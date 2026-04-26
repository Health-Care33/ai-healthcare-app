from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    google_id: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    