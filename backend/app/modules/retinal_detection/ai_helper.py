import requests
import os

API_KEY = os.getenv("GROQ_API_KEY")


def get_ai_medical_report(disease, confidence):

    print("🔑 API KEY:", API_KEY)

    if not API_KEY:
        print("❌ API KEY NOT FOUND")
        return fallback_response(disease)

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

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
2. Future Risks:
3. Treatment:
4. Prevention:
5. Doctor Recommendation:
"""

        data = {
            "model": "llama-3.1-8b-instant",  # ✅ FINAL WORKING MODEL
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        print("📡 Sending request to Groq...")

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=15
        )

        print("📥 Status Code:", response.status_code)
        print("📥 Response Text:", response.text)

        if response.status_code != 200:
            print("❌ Groq API Error")
            return fallback_response(disease)

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]

        return fallback_response(disease)

    except Exception as e:
        print("❌ Exception:", str(e))
        return fallback_response(disease)


def fallback_response(disease):
    return f"""
Disease: {disease}

⚠️ AI service unavailable.

👉 Please consult an ophthalmologist.
👉 Maintain regular eye checkups.
"""