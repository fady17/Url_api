from fastapi import APIRouter
from app.api.v1.endpoints import url_check, results, users

api_router = APIRouter()
api_router.include_router(url_check.router, prefix="/url_check", tags=["URL Check"])
api_router.include_router(results.router, prefix="/results", tags=["Results"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
