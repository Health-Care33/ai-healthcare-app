from pydantic import BaseModel, Field
from typing import Optional


# 🔥 API RESPONSE SCHEMA
class FingerprintPredictionResponse(BaseModel):
    success: bool = Field(..., example=True)
    blood_group: str = Field(..., example="A")  # ✅ fixed
    confidence: float = Field(..., example=92.5)
    message: str = Field(..., example="Prediction successful")


# 🔥 DB SCHEMA
class FingerprintPredictionDB(BaseModel):
    user_id: Optional[str] = None
    type: str = "fingerprint"
    blood_group: str
    confidence: float
    file: Optional[str] = None