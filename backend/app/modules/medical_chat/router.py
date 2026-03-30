from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.medical_chat.ai_engine import analyze_medical_report
from app.modules.medical_chat.diagnosis_engine import generate_diagnosis

# Router create
router = APIRouter()


# ---------------- CHAT REQUEST ----------------

class ChatRequest(BaseModel):
    report_text: str
    question: str


# ---------------- DIAGNOSIS REQUEST ----------------

class DiagnosisRequest(BaseModel):
    report_text: str


# ---------------- MEDICAL AI CHAT ----------------

@router.post("/ask")
def ask_medical_ai(data: ChatRequest):

    answer = analyze_medical_report(
        report_text=data.report_text,
        question=data.question
    )

    if "AI Error" in answer:
        return {
            "success": False,
            "error": answer
        }

    return {
        "success": True,
        "question": data.question,
        "answer": answer
    }


# ---------------- AI DIAGNOSIS ----------------

@router.post("/diagnose")
def ai_diagnosis(data: DiagnosisRequest):

    diagnosis = generate_diagnosis(
        report_text=data.report_text
    )

    return {
        "diagnosis": diagnosis
    }