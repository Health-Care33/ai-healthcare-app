from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config.settings import settings

from app.routes.auth_routes import router as auth_router
from app.routes.analytics import router as analytics_router

from app.modules.fingerprint.router import router as fingerprint_router
from app.modules.medical_reports.router import router as medical_report_router
from app.modules.medical_chat.router import router as medical_chat_router
from app.modules.health_risk.router import router as health_risk_router
from app.modules.blood_donation.router import router as blood_donation_router
from app.modules.retinal_detection.router import router as retinal_router


app = FastAPI(title="AI Healthcare Backend")


# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Session (SECURE)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET
)


# ✅ ROUTES
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(fingerprint_router, prefix="/api/fingerprint", tags=["Fingerprint"])
app.include_router(medical_report_router, prefix="/api/medical-report", tags=["Medical Reports"])
app.include_router(medical_chat_router, prefix="/api/medical-chat", tags=["Medical Chat"])
app.include_router(health_risk_router, prefix="/api/health-risk", tags=["Health Risk"])
app.include_router(blood_donation_router, prefix="/api/blood-donation", tags=["Blood Donation"])
app.include_router(analytics_router, prefix="/api/admin", tags=["Admin"])
app.include_router(retinal_router, prefix="/api/retinal", tags=["Retinal Detection"])


@app.get("/")
def root():
    return {"message": "Backend Running 🚀"}