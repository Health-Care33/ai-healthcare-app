from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = None

if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    print("⚠️ GROQ API KEY NOT FOUND")


# 🔥 MAIN FUNCTION (UNIFIED)
def medical_ai_analysis(report_text: str, question: str = None):

    if not client:
        return fallback_response()

    try:
        if question:
            # 🔥 Q&A MODE
            prompt = f"""
You are an expert medical AI assistant.

Medical Report:
{report_text}

User Question:
{question}

Instructions:
- Answer in simple language
- Highlight abnormal values
- Avoid dangerous advice
- Suggest doctor consultation
"""
        else:
            # 🔥 AUTO ANALYSIS MODE
            prompt = f"""
You are a professional medical AI.

Analyze the report and provide:

1. Abnormal values
2. Possible health risks
3. Simple explanation
4. Doctor consultation advice

Report:
{report_text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful medical AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        if response and response.choices:
            return response.choices[0].message.content

        return fallback_response()

    except Exception as e:
        print("⚠️ GROQ ERROR:", e)
        return fallback_response()


def fallback_response():
    return """
⚠️ AI service is temporarily unavailable.

👉 Please consult a qualified doctor.
👉 Ensure regular health checkups.
"""