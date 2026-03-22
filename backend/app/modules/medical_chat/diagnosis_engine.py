import os
from groq import Groq

# SAFE API KEY (from .env)
client = Groq(
    api_key=os.getenv("API_KEY")
)

def generate_diagnosis(report_text):

    prompt = f"""
You are a professional medical AI.

Analyze the following medical report and provide:

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
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content