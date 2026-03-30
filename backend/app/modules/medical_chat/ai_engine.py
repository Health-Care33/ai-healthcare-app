import os
from groq import Groq


def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY not set")

    return Groq(api_key=api_key)


def analyze_medical_report(report_text: str, question: str):

    try:
        client = get_client()

        prompt = f"""
Medical Report:
{report_text}

Question:
{question}

Explain in simple terms for a patient.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ GROQ ERROR: {e}")
        return f"AI Error: {str(e)}"