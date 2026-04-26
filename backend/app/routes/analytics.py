from fastapi import APIRouter

from app.database.mongodb import (
    user_collection,
    prediction_collection,
    medical_report_collection,
    blood_check_collection
)

router = APIRouter()


@router.get("/analytics")
async def get_admin_analytics():

    total_users = await user_collection.count_documents({})

    fingerprint_predictions = await prediction_collection.count_documents({
        "type": "fingerprint"
    })

    retinal_scans = await prediction_collection.count_documents({
        "type": "retina"
    })

    medical_reports = await medical_report_collection.count_documents({})

    blood_checks = await blood_check_collection.count_documents({})

    return {
        "total_users": total_users,
        "fingerprint_predictions": fingerprint_predictions,
        "retinal_scans": retinal_scans,
        "medical_reports": medical_reports,
        "blood_checks": blood_checks
    }