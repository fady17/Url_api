from fastapi import Depends, HTTPException

def get_api_key_header(api_key: str = Depends(...)):
    if api_key != "expected_api_key":
        raise HTTPException(status_code=403, detail="Invalid API key.")
    return api_key
