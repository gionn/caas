import os
import redis


REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(REDIS_URL)


if __name__ == '__main__':
    redis.ping()
