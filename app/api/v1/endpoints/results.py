from fastapi import APIRouter, HTTPException, Query
from app.db.mongodb import get_mongo_client
from app.models.url_check import URLCheckModel

router = APIRouter()


@router.get("/results")
async def get_scan_results(url: str):
    # Get the scan results from MongoDB
    client = get_mongo_client()
    url_check_collection = client["url_integrity_checker"]["url_checks"]

    # Fetch the result for the given URL
    result = url_check_collection.find_one({"url": url})

    if not result:
        raise HTTPException(status_code=404, detail="No scan results found for this URL.")

    return {
        "url": result["url"],
        "status": result["status"],
        "positives": result["positives"],
        "total": result["total"],
        "scan_date": result["scan_date"],
        "permalink": result["permalink"]
    }
