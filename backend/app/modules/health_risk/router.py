from fastapi import APIRouter
from app.modules.health_risk.schema import HealthRiskInput
from app.modules.health_risk.predictor import predict_health_risk
from app.modules.health_risk.service import save_prediction

router = APIRouter()

@router.post("/predict")
async def predict_risk(data: HealthRiskInput):

    result = predict_health_risk(data)

    # temporary user id
    user_id = "demo_user"

    await save_prediction(
        user_id,
        data.dict(),
        result
    )

    return {
        "success": True,
        "prediction": result
    }