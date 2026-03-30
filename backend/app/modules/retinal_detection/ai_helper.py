import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")  # ✅ FIXED


def get_ai_medical_report(disease, confidence):

    if not API_KEY:
        return "⚠️ AI service not configured."

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""
You are a professional eye specialist.

Disease: {disease}
Confidence: {confidence}%

Explain:
1. Overview
2. Risks
3. Treatment
4. Prevention
5. Doctor
"""

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI Error:", e)

        return f"""
Disease: {disease}

⚠️ AI unavailable. Please consult a doctor.
"""