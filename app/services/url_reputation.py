import requests
import hashlib
from app.core.config import settings
from app.core.cache import get_cache, set_cache


class VirusTotalError(Exception):
    pass


class RateLimitError(VirusTotalError):
    pass


BASE_URL = "https://www.virustotal.com/vtapi/v2"


def make_vt_request(endpoint: str, params: dict) -> dict:
    cache_key = f"vt:{endpoint}:{hashlib.md5(str(params).encode()).hexdigest()}"
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    url = f"{BASE_URL}/{endpoint}"
    params["apikey"] = settings.VIRUSTOTAL_API_KEY

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            set_cache(cache_key, result)
            return result
        elif response.status_code == 204:
            raise RateLimitError("API request rate limit exceeded")
        elif response.status_code == 403:
            raise VirusTotalError("Invalid API key")
        else:
            raise VirusTotalError(f"API error: {response.status_code}")
    except requests.RequestException as e:
        raise VirusTotalError(f"Network error: {str(e)}")


def get_url_report(url: str) -> dict:
    return make_vt_request("url/report", {"resource": url})


def get_file_report(file_hash: str) -> dict:
    return make_vt_request("file/report", {"resource": file_hash})


def get_domain_report(domain: str) -> dict:
    return make_vt_request("domain/report", {"domain": domain})


def get_ip_report(ip: str) -> dict:
    return make_vt_request("ip-address/report", {"ip": ip})


def process_vt_response(result: dict) -> dict:
    response_code = result.get("response_code", -1)
    if response_code == 0:
        return {"status": "Not found in database", "scan_date": None, "permalink": None}

    positives = result.get("positives", 0)
    total = result.get("total", 0)

    if positives == 0:
        status = "Clean"
    elif positives < 3:
        status = "Suspicious"
    else:
        status = "Malicious"

    return {
        "status": status,
        "positives": positives,
        "total": total,
        "scan_date": result.get("scan_date"),
        "permalink": result.get("permalink"),
        "scans": result.get("scans", {}),
        "additional_info": result.get("additional_info", {})
    }