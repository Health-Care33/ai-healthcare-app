from fastapi import APIRouter, HTTPException
from app.modules.health_risk.schema import HealthRiskInput
from app.modules.health_risk.predictor import predict_health_risk
from app.modules.health_risk.service import save_prediction

router = APIRouter(tags=["Health Risk"])


@router.post("/predict")
async def predict_risk(data: HealthRiskInput):

    try:
        # ================= INPUT =================
        input_data = data.model_dump()

        # ================= PREDICTION =================
        result = predict_health_risk(input_data)

        # strict error handling
        if not result or result.get("error"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Prediction failed")
            )

        # ================= USER (TEMP) =================
        user_id = "demo_user"

        # ================= SAVE TO DB =================
        try:
            await save_prediction(
                user_id,
                input_data,
                {
                    "risk_level": result.get("risk_level"),
                    "confidence": result.get("confidence"),
                    "possible_diseases": result.get("possible_diseases")
                }
            )
        except Exception as db_error:
            print("⚠️ DB Error:", db_error)

        # ================= FINAL RESPONSE =================
        return {
            "success": True,
            "prediction": result.get("risk_level"),
            "confidence": result.get("confidence"),
            "possible_diseases": result.get("possible_diseases")
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ Router Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")