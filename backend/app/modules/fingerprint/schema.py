from pydantic import BaseModel, Field
from typing import Optional, List


# ================= TOP-2 PREDICTION =================
class TopPrediction(BaseModel):
    blood_group: str = Field(..., example="A+")
    confidence: float = Field(..., ge=0, le=100, example=85.3)


# ================= API RESPONSE =================
class FingerprintPredictionResponse(BaseModel):
    success: bool = Field(..., example=True)

    blood_group: Optional[str] = Field(default=None, example="A+")   # ✅ FIX
    confidence: Optional[float] = Field(default=None, ge=0, le=100)  # ✅ FIX

    warning: Optional[str] = Field(default=None)
    top_2: List[TopPrediction] = Field(default_factory=list)         # ✅ FIX

    error: Optional[str] = None   # 🔥 IMPORTANT (for failure cases)


# ================= DB SCHEMA =================
class FingerprintPredictionDB(BaseModel):
    user_id: Optional[str] = None

    type: str = "fingerprint"
    file: Optional[str] = None

    blood_group: Optional[str] = None     # ✅ FIX
    confidence: Optional[float] = None    # ✅ FIX

    warning: Optional[str] = None
    top_2: List[TopPrediction] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }