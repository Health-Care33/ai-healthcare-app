from fastapi import APIRouter
from app.modules.blood_donation.service import process_blood_compatibility
from app.modules.blood_donation.schema import BloodCompatibilityRequest

router = APIRouter()

@router.post("/check")
async def check_blood_compatibility(data: BloodCompatibilityRequest):

    result = await process_blood_compatibility(data.blood_group)

    return {
        "success": True,
        "data": result
    }