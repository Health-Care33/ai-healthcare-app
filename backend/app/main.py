from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
import gdown   # ✅ FIX: requests → gdown

# 🔥 LOAD ENV
load_dotenv()


# ---------------- DOWNLOAD FUNCTION ----------------
def download_model(file_id, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        print(f"📥 Downloading {path}...")

        try:
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, path, quiet=False)   # ✅ FIX
            print(f"✅ Download complete: {path}")

        except Exception as e:
            print("❌ Download failed:", e)
            raise e   # ✅ IMPORTANT (fail loudly)

    else:
        print(f"⚡ Model already exists: {path}")


# ---------------- FASTAPI APP ----------------
app = FastAPI(
    title="AI Based Healthcare System",
    description="Full Stack AI Healthcare Backend using FastAPI",
    version="1.0.0"
)


# ---------------- ROUTES (IMPORT SAFE ORDER) ----------------
from app.routes.auth_routes import router as auth_router
from app.routes.analytics import router as analytics_router

from app.modules.fingerprint.router import router as fingerprint_router
from app.modules.medical_reports.router import router as medical_report_router
from app.modules.medical_chat.router import router as medical_chat_router
from app.modules.health_risk.router import router as health_risk_router
from app.modules.blood_donation.router import router as blood_donation_router
from app.modules.retinal_detection.model.router import router as retinal_router


# ---------------- STARTUP EVENT ----------------
@app.on_event("startup")
async def startup_event():
    print("🚀 Server started successfully")

    # 🔥 MODEL DOWNLOADS (FIXED)
    download_model(
        "1lxXyTLMng59RBRzgpLy_Oyv6n7TG3Fzz",
        "app/modules/retinal_detection/model/retina_validation_model.h5"
    )

    download_model(
        "1Cq9O5-A3DBv7llh6oo1C06cqnMgUovmz",
        "app/modules/fingerprint/model/fingerprint_validation_model.h5"
    )

    # ---------------- LOAD MODELS ----------------
    try:
        from app.modules.retinal_detection.model.predictor import load_retinal_model
        load_retinal_model()
        print("✅ Retinal model preloaded")
    except Exception as e:
        print("❌ Retinal model error:", e)

    # 🔥 NEW FIX (VALIDATION MODEL LOAD)
    try:
        from app.modules.retinal_detection.model.retina_validation import load_validation_model
        load_validation_model()
        print("✅ Retina validation model preloaded")
    except Exception as e:
        print("❌ Retina validation model error:", e)

    try:
        from app.modules.fingerprint.predictor import load_fingerprint_model
        load_fingerprint_model()
        print("✅ Fingerprint model preloaded")
    except Exception as e:
        print("❌ Fingerprint model error:", e)

    try:
        from app.modules.health_risk.predictor import load_health_model
        load_health_model()
        print("✅ Health Risk model preloaded")
    except Exception as e:
        print("❌ Health model error:", e)


# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- SESSION ----------------
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret-key-change-this"),
    same_site="none",
    https_only=True
)


# ---------------- ROUTES REGISTER ----------------
app.include_router(auth_router, prefix="/api/auth")
app.include_router(fingerprint_router, prefix="/api/fingerprint")
app.include_router(medical_report_router, prefix="/api/medical-report")
app.include_router(medical_chat_router, prefix="/api/medical-chat")
app.include_router(health_risk_router, prefix="/api/health-risk")
app.include_router(blood_donation_router, prefix="/api/blood-donation")
app.include_router(analytics_router, prefix="/api/admin")
app.include_router(retinal_router, prefix="/api/retinal")


# ---------------- ROOT ----------------
@app.get("/")
async def root():
    return {"message": "AI Healthcare Backend Running Successfully 🚀"}


# ---------------- HEALTH CHECK ----------------
@app.get("/health")
async def health():
    return {"status": "ok"}