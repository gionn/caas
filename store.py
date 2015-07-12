import redis

from config import REDIS_URL


redis = redis.from_url(REDIS_URL)
