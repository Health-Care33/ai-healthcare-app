from datetime import datetime
from app.database.mongodb import db
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

collection = db["health_risk_predictions"]

# ================= GROQ CLIENT =================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


# ================= AI FUNCTION =================
def get_ai_disease_prediction(input_data, result):

    # 🔥 API KEY CHECK
    if not os.getenv("GROQ_API_KEY"):
        return "AI service unavailable (missing GROQ_API_KEY)"

    prompt = f"""
Patient Health Data:
{input_data}

Prediction Result:
{result}

Task:
- Suggest possible future diseases
- Give short bullet points only
- No extra explanation
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a medical AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=250
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ Groq Error:", e)
        return "AI prediction unavailable"


# ================= SAVE FUNCTION =================
async def save_prediction(user_id, input_data, result):

    try:
        ai_response = get_ai_disease_prediction(input_data, result)

        document = {
            "user_id": user_id,
            "type": "health_risk",
            "input_data": input_data,
            "prediction": result,
            "ai_response": ai_response,
            "created_at": datetime.utcnow()
        }

        await collection.insert_one(document)

        return {
            "success": True,
            "prediction": result,
            "ai_response": ai_response
        }

    except Exception as e:
        print("❌ Service Error:", e)

        return {
            "success": False,
            "error": str(e)
        }