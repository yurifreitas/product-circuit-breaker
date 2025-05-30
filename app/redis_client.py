import redis
import json
import os
from datetime import timedelta


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def get_from_redis_cache(key: str):

    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

def store_in_redis_cache(key: str, data: list):

    redis_client.setex(key, timedelta(minutes=10), json.dumps(data))
