from pydantic import BaseModel, Field
from typing import Optional, List


# ================= TOP-2 =================
class TopPrediction(BaseModel):
    blood_group: str = Field(..., example="A+")
    confidence: float = Field(..., ge=0, le=100, example=85.3)


# ================= API RESPONSE =================
class FingerprintPredictionResponse(BaseModel):
    success: bool = Field(..., example=True)

    blood_group: str = Field(default="Unknown", example="A+")
    confidence: float = Field(default=0.0, ge=0, le=100)

    warning: Optional[str] = None
    top_2: List[TopPrediction] = Field(default_factory=list)

    error: Optional[str] = None
    details: Optional[str] = None   # 🔥 for debug / logs


# ================= DB SCHEMA =================
class FingerprintPredictionDB(BaseModel):
    user_id: Optional[str] = None

    type: str = "fingerprint"
    file: Optional[str] = None

    blood_group: str = "Unknown"
    confidence: float = 0.0

    warning: Optional[str] = None
    top_2: List[TopPrediction] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }