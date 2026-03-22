import requests

API_KEY = "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"

def get_ai_medical_report(disease, confidence):

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
            "model": "openai/gpt-3.5-turbo",  # free/cheap model
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

        ⚠️ AI service unavailable.

        👉 Please consult an ophthalmologist.
        👉 Maintain regular eye checkups.
        """