from fastapi import APIRouter, HTTPException
from app.modules.health_risk.schema import HealthRiskInput
from app.modules.health_risk.predictor import predict_health_risk
from app.modules.health_risk.service import save_prediction

router = APIRouter(tags=["Health Risk"])


@router.post("/predict")
async def predict_risk(data: HealthRiskInput):

    try:
        # ✅ convert request to dict
        input_data = data.dict()

        # 🔥 ML + GROQ prediction
        result = predict_health_risk(input_data)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # 🔥 temp user (replace later with auth)
        user_id = "demo_user"

        # ✅ CLEAN DB SAVE
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

        # ✅ FINAL RESPONSE
        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))