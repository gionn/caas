import os


REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
SECRET_KEY = os.getenv('SECRET_KEY', 'GIAO')
