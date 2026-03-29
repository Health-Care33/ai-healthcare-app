import pytesseract
from pdf2image import convert_from_path
import os

# ✅ Windows only
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(pdf_path: str):

    extracted_text = ""

    try:
        images = convert_from_path(pdf_path)

        for img in images:
            text = pytesseract.image_to_string(img)
            extracted_text += text + "\n"

        return extracted_text

    except Exception as e:
        return f"OCR Error: {str(e)}"