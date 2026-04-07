from groq import Groq
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = None

# ✅ safe client init
if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    print("⚠️ GROQ API KEY NOT FOUND")


# ---------------- AI ANALYSIS FUNCTION ---------------- #

def analyze_medical_report(report_text: str, question: str):

    if not client:
        return fallback_response()

    try:
        prompt = f"""
You are an expert medical AI assistant.

A user uploaded a medical report. The OCR extracted text is below.

Medical Report:
{report_text}

User Question:
{question}

Instructions:
- Explain in simple language
- Highlight abnormal values clearly
- Do NOT give dangerous medical advice
- Suggest consulting a doctor if needed
- Keep answer structured and easy to read
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful medical AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800,
        )

        # ✅ safe parsing
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