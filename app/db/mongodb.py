from pymongo import MongoClient
from app.core.config import settings

def get_mongo_client() -> MongoClient:
    return MongoClient(settings.MONGO_URL)
