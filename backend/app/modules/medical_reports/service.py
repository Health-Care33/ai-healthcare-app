import os
from datetime import datetime
from fastapi import UploadFile
from app.modules.medical_reports.ocr_engine import extract_text_from_pdf
from app.database.mongodb import medical_report_collection

UPLOAD_DIR = "app/modules/medical_reports/uploads"


async def save_medical_report(file: UploadFile):

    # folder create
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # OCR run
    extracted_text = extract_text_from_pdf(file_path)

    # MongoDB save
    data = {
        "file_name": file.filename,
        "file_path": file_path,
        "extracted_text": extracted_text,
        "created_at": datetime.utcnow()
    }

    await medical_report_collection.insert_one(data)

    return {
        "message": "Medical report processed successfully",
        "file_name": file.filename,
        "extracted_text": extracted_text
    }