from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# ----------- ROUTE IMPORTS -----------

from app.routes.auth_routes import router as auth_router
from app.routes.analytics import router as analytics_router

# 🔥 FIXED IMPORT
from app.modules.fingerprint.router import router as fingerprint_router

from app.modules.medical_reports.router import router as medical_report_router
from app.modules.medical_chat.router import router as medical_chat_router
from app.modules.health_risk.router import router as health_risk_router
from app.modules.blood_donation.router import router as blood_donation_router

from app.modules.retinal_detection.model.router import router as retinal_router


# ----------- FASTAPI APP -----------

app = FastAPI(
    title="AI Based Healthcare System",
    description="Full Stack AI Healthcare Backend using FastAPI",
    version="1.0.0"
)

# ----------- CORS -----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- SESSION -----------

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this"
)

# ----------- ROUTES -----------

app.include_router(auth_router, prefix="/api/auth")

app.include_router(fingerprint_router, prefix="/api/fingerprint")

app.include_router(medical_report_router, prefix="/api/medical-report")

app.include_router(medical_chat_router, prefix="/api/medical-chat")

app.include_router(health_risk_router, prefix="/api/health-risk")

app.include_router(blood_donation_router, prefix="/api/blood-donation")

app.include_router(analytics_router, prefix="/api/admin")

# 🔥 RETINAL DETECTION ROUTE
app.include_router(retinal_router, prefix="/api")

# ----------- ROOT -----------

@app.get("/")
def root():
    return {
        "message": "AI Healthcare Backend Running Successfully 🚀"
    }