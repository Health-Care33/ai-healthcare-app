from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.modules.medical_chat.ai_engine import medical_ai_analysis

router = APIRouter(tags=["Medical Chat"])


# ---------------- REQUEST SCHEMAS ----------------

class ChatRequest(BaseModel):
    report_text: str
    question: str


class DiagnosisRequest(BaseModel):
    report_text: str


# ---------------- MEDICAL AI CHAT ----------------

@router.post("/ask")
async def ask_medical_ai(data: ChatRequest):

    try:
        answer = medical_ai_analysis(
            report_text=data.report_text,
            question=data.question
        )

        return {
            "success": True,
            "question": data.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- AI DIAGNOSIS ----------------

@router.post("/diagnose")
async def ai_diagnosis(data: DiagnosisRequest):

    try:
        diagnosis = medical_ai_analysis(
            report_text=data.report_text
        )

        return {
            "success": True,
            "diagnosis": diagnosis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))