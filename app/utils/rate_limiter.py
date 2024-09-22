from app.db.redis import redis


async def is_rate_limited(user_id: str, limit: int = 100, period: int = 3600):
    key = f"rate_limit:{user_id}"
    current_count = await redis.get(key)

    if current_count and int(current_count) >= limit:
        return True

    await redis.incr(key)
    await redis.expire(key, period)

    return False
