import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OCR_API_KEY")


def extract_text_from_pdf(pdf_path: str):
    try:
        url = "https://api.ocr.space/parse/image"

        with open(pdf_path, "rb") as f:
            response = requests.post(
                url,
                files={"file": f},
                data={
                    "apikey": API_KEY,
                    "language": "eng"
                }
            )

        result = response.json()

        if result.get("IsErroredOnProcessing"):
            return f"OCR Error: {result.get('ErrorMessage')}"

        parsed_text = ""

        for item in result.get("ParsedResults", []):
            parsed_text += item.get("ParsedText", "") + "\n"

        return parsed_text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"