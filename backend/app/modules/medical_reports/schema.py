from pydantic import BaseModel

class MedicalReportResponse(BaseModel):
    message: str
    file_name: str