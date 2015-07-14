import os


def get_first_env(keys, default):
    for key in keys:
        if key in os.environ:
            return os.getenv(key)

    return default


REDIS_URL = get_first_env(['REDISTOGO_URL', 'REDIS_URL'], 'redis://localhost:6379')
SECRET_KEY = os.getenv('SECRET_KEY', 'GIAO')
