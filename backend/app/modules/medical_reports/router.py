from fastapi import APIRouter, UploadFile, File
from app.modules.medical_reports.service import save_medical_report

router = APIRouter(tags=["Medical Reports"])


@router.post("/upload")
async def upload_medical_report(file: UploadFile = File(...)):

    result = await save_medical_report(file)

    return {
        "success": True,
        "data": result
    }