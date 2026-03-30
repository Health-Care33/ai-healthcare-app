import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")  # ✅ FIXED
)

def analyze_medical_report(report_text: str, question: str):

    try:
        prompt = f"""
Medical Report:
{report_text}

Question:
{question}
Explain simply.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"