from pydantic import BaseModel, Field
from typing import Optional, List


# ================= TOP-2 PREDICTION =================
class TopPrediction(BaseModel):
    blood_group: str = Field(..., example="A+")
    confidence: float = Field(..., ge=0, le=100, example=85.3)


# ================= API RESPONSE =================
class FingerprintPredictionResponse(BaseModel):
    success: bool = Field(..., example=True)
    blood_group: str = Field(..., example="A+")
    confidence: float = Field(..., ge=0, le=100, example=92.5)
    warning: Optional[str] = Field(default=None)
    top_2: Optional[List[TopPrediction]] = Field(default_factory=list)


# ================= DB SCHEMA =================
class FingerprintPredictionDB(BaseModel):
    user_id: Optional[str] = None

    type: str = "fingerprint"
    file: Optional[str] = None

    blood_group: str
    confidence: float

    warning: Optional[str] = None
    top_2: List[TopPrediction] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }