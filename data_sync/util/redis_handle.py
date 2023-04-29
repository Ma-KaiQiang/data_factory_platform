from django_redis import get_redis_connection
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'data_factory_platform.settings'


# conn = cache.get()
# conn.hset('auth', 'headers', '019230124')
# a = conn.hgetall('auth')
class RedisHandle():
    def __init__(self):
        self.client = get_redis_connection()
