from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCheckRequestModel(BaseModel):
    url: HttpUrl  # Validates the input as a proper URL

class URLCheckResponseModel(BaseModel):
    url: str
    status: str
    positives: int
    total: int
    scan_date: datetime
    permalink: str

    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com",
                "status": "malicious",
                "positives": 5,
                "total": 70,
                "scan_date": "2024-01-01T00:00:00Z",
                "permalink": "https://www.virustotal.com/gui/url/abcdefg"
            }
        }
