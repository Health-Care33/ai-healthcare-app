import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_ai_medical_report(disease, confidence):

    # ✅ API key check
    if not API_KEY:
        return fallback_response(disease)

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""
You are a professional eye specialist.

Patient has:
Disease: {disease}
Confidence: {confidence}%

Give response in this EXACT format:

1. Disease Overview:
(Explain simply)

2. Future Risks:
(What can happen if ignored)

3. Treatment:
(Medication / surgery if needed)

4. Prevention:
(How to avoid worsening)

5. Doctor Recommendation:
(Which specialist to visit)

Keep each section short and clear.
"""

        data = {
            "model": "openai/gpt-4o-mini",  # 🔥 updated model
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10  # ✅ prevent hanging
        )

        result = response.json()

        # ✅ safe parsing
        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        else:
            print("⚠️ Invalid API response:", result)
            return fallback_response(disease)

    except Exception as e:
        print("AI Error:", e)
        return fallback_response(disease)


def fallback_response(disease):
    return f"""
Disease: {disease}

⚠️ AI service unavailable.

👉 Please consult an ophthalmologist.
👉 Maintain regular eye checkups.
"""