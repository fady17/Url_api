import aioredis
from app.core.config import settings
import json

redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_cache(key: str):
    value = await redis.get(key)
    if value:
        return json.loads(value)
    return None

async def set_cache(key: str, value: dict, expiration: int = 3600):
    await redis.setex(key, expiration, json.dumps(value))
