from fastapi import APIRouter, HTTPException, Query
from app.models.pydantic.url_check import URLCheckRequestModel, URLCheckResponseModel
from app.models.url_check import URLCheckModel
from app.services.url_reputation import get_url_report, process_vt_response, VirusTotalError, RateLimitError
from app.db.redis import set_cache, get_cache
from app.db.mongodb import get_mongo_client

router = APIRouter()

@router.post("/scan", response_model=URLCheckResponseModel)
async def scan_url(request: URLCheckRequestModel, detailed: bool = Query(False, description="Include detailed scan results")):
    url = request.url
    # Check Redis cache first
    cached_result = await get_cache(str(url))
    if cached_result:
        return cached_result

    try:
        # Check URL report via VirusTotal
        reputation_result = get_url_report(str(url))

        # Process the VirusTotal response
        processed_result = process_vt_response(reputation_result)

        # Store result in MongoDB
        client = get_mongo_client()
        url_check_collection = client["url_integrity_checker"]["url_checks"]
        url_check_data = URLCheckModel(
            url=str(url),
            status=processed_result["status"],
            positives=processed_result["positives"],
            total=processed_result["total"],
            scan_date=processed_result["scan_date"],
            permalink=processed_result["permalink"]
        )
        url_check_collection.insert_one(url_check_data.dict())

        # Cache result in Redis
        await set_cache(str(url), processed_result)

        # Return the result
        return URLCheckResponseModel(
            url=str(url),
            status=processed_result["status"],
            positives=processed_result["positives"],
            total=processed_result["total"],
            scan_date=processed_result["scan_date"],
            permalink=processed_result["permalink"]
        )

    except RateLimitError:
        raise HTTPException(status_code=429, detail="API rate limit exceeded. Please try again later.")
    except VirusTotalError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
