import redis

from config import REDIS_URL


_redis = redis.from_url(REDIS_URL)


def get(label):
    counter = _redis.get(label)

    if counter is None:
        counter = 0

    return int(counter)


def incr(label):
    return _redis.incr(label)


def set(label, counter):
    _redis.set(label, counter)


def delete(label):
    _redis.delete(label)
