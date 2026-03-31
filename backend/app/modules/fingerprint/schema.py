from pydantic import BaseModel
from typing import Optional


class FingerprintPredictionResponse(BaseModel):
    blood_group: str
    confidence: float
    message: str


class FingerprintPredictionDB(BaseModel):
    user_id: str
    blood_group: str
    confidence: float
    image_path: Optional[str] 