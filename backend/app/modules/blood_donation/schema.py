# backend/app/modules/blood_donation/schema.py

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class BloodCompatibilityRequest(BaseModel):
    """
    Request schema for blood compatibility check
    """

    blood_group: str = Field(
        ...,
        example="A+",
        description="User blood group"
    )


class BloodCompatibilityResponse(BaseModel):
    """
    Response schema returned to frontend
    """

    blood_group: str

    can_donate_to: List[str]

    can_receive_from: List[str]


class BloodCompatibilityDB(BaseModel):
    """
    Schema for storing compatibility queries in MongoDB
    """

    user_id: str

    blood_group: str

    can_donate_to: List[str]

    can_receive_from: List[str]

    created_at: datetime = Field(default_factory=datetime.utcnow)