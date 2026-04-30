from pydantic import BaseModel, Field, field_validator


class HealthRiskInput(BaseModel):

    age: int = Field(..., ge=0, le=120, example=25)
    bmi: float = Field(..., ge=5, le=60, example=22.5)

    blood_pressure: float = Field(..., ge=40, le=250, example=120)
    cholesterol: float = Field(..., ge=50, le=400, example=180)
    glucose: float = Field(..., ge=30, le=500, example=90)

    smoking: int = Field(..., ge=0, le=1, example=0)
    alcohol: int = Field(..., ge=0, le=1, example=0)
    physical_activity: int = Field(..., ge=0, le=1, example=1)

    gender: int = Field(..., ge=0, le=1, example=1)  # 0 = female, 1 = male


    # ================= OPTIONAL SAFETY VALIDATION =================
    @field_validator("bmi")
    @classmethod
    def check_bmi(cls, v):
        if v <= 0:
            raise ValueError("BMI must be positive")
        return v


# ================= RESPONSE SCHEMA =================
class HealthRiskResponse(BaseModel):

    success: bool = True
    prediction: str
    ai_response: str
    error: str | None = None