import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")  # ✅ FIXED
)

def generate_diagnosis(report_text):

    try:
        prompt = f"""
Analyze report:

{report_text}
Give risks + explanation.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Diagnosis Error: {str(e)}"