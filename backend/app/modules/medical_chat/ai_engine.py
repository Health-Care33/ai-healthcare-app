from groq import Groq
import os
from dotenv import load_dotenv
import re

# ---------------- LOAD ENV ---------------- #
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

client = None
if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    print("⚠️ GROQ API KEY NOT FOUND")


# ---------------- FORMAT FUNCTION ---------------- #
def format_response(text):
    # Convert **bold** → <b>bold</b>
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Convert new lines → HTML paragraph breaks
    text = text.replace("\n", "<br><br>")

    return text


# ---------------- CORE AI FUNCTION ---------------- #
def medical_chat(question: str):

    if not client:
        return fallback_response()

    try:
        prompt = f"""
You are a professional and friendly medical assistant.

User Question:
{question}

Instructions:
- Understand the intent even if the user uses simple, broken, or informal language
- If the question is health-related, give a helpful and clear answer
- If NOT health-related, reply ONLY:
"I only provide health-related information."

- Explain in simple language
- Mention possible causes if relevant
- Keep answer natural and human-like
- Use short paragraphs
- Highlight important medical terms using **bold**
- Use a few relevant emojis 🙂
- Suggest consulting a doctor when necessary
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ working model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert medical assistant who understands all kinds of health-related questions, even if they are unclear or informal."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=700,
        )

        if response and response.choices:
            raw_text = response.choices[0].message.content
            return format_response(raw_text)   # ✅ HTML output

        return fallback_response()

    except Exception as e:
        print("⚠️ GROQ ERROR:", e)
        return fallback_response()


# ---------------- WRAPPER ---------------- #
def medical_ai_analysis(report_text: str, question: str):
    return medical_chat(question)


# ---------------- FALLBACK ---------------- #
def fallback_response():
    return """
⚠️ AI service is temporarily unavailable.<br><br>

👉 Please consult a qualified doctor.<br>
👉 Ensure regular health checkups.
"""