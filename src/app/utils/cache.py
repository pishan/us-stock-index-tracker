import redis
import json
import hashlib
import os


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


def cache_result(func):
    def wrapper(*args, **kwargs):
        key = hashlib.md5((func.__name__ + str(args) + str(kwargs)).encode()).hexdigest()
        if r.exists(key):
            return json.loads(r.get(key))
        result = func(*args, **kwargs)
        r.set(key, json.dumps(result))
        return result
    return wrapper
