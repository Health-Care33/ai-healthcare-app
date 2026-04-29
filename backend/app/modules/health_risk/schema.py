from pydantic import BaseModel, Field


class HealthRiskInput(BaseModel):
    age: int = Field(..., example=25)
    bmi: float = Field(..., example=22.5)
    blood_pressure: float = Field(..., example=120)
    cholesterol: float = Field(..., example=180)
    glucose: float = Field(..., example=90)
    smoking: int = Field(..., example=0)
    alcohol: int = Field(..., example=0)
    physical_activity: int = Field(..., example=1)
    gender: int = Field(..., example=1)  # ✅ ADD THIS