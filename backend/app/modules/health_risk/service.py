from datetime import datetime
from app.database.mongodb import db

# ✅ NEW IMPORTS
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

collection = db["health_risk_predictions"]


# ✅ NEW FUNCTION (AI DISEASE SUGGESTION)
def get_ai_disease_prediction(input_data, result):

    prompt = f"""
    Patient Health Data:
    {input_data}

    Prediction Result:
    {result}

    Based on this, suggest possible future diseases.
    Give short bullet points only.
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq Error:", e)
        return "AI prediction unavailable"


# ✅ EXISTING FUNCTION (UNCHANGED)
async def save_prediction(user_id, input_data, result):

    document = {
        "user_id": user_id,
        "type": "health_risk",
        "input_data": input_data,
        "prediction": result,
        "created_at": datetime.utcnow()
    }

    try:
        await collection.insert_one(document)
    except Exception as e:
        print("⚠️ MongoDB Error:", e)

    return document