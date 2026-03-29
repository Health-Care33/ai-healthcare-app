import os
from groq import Groq

# ✅ FIXED ENV VARIABLE
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_medical_report(report_text: str, question: str):

    prompt = f"""
You are an expert medical AI assistant.

Medical Report:
{report_text}

User Question:
{question}

Instructions:
- Explain in simple language
- If values are abnormal explain possible meaning
- Do NOT give dangerous medical advice
- Suggest consulting a doctor if needed
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

    return response.choices[0].message.content