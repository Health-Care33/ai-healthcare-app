from pydantic import BaseModel


class HealthRiskInput(BaseModel):

    age: int
    gender: int
    bmi: float
    blood_pressure: float
    cholesterol: float
    glucose: float
    heart_rate: float
    smoking: int
    activity: int 