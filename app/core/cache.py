import redis
import json
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cache(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key: str, value: dict, expiration: int = 3600):
    redis_client.setex(key, expiration, json.dumps(value))