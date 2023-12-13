import redis

API = ""
REDIS_CLOUD_HOST = ""
REDIS_CLOUD_PORT = 10109
REDIS_CLOUD_PASSWORD = ""

redis_conn = redis.StrictRedis(
    host=REDIS_CLOUD_HOST,
    port=REDIS_CLOUD_PORT,
    password=REDIS_CLOUD_PASSWORD,
    decode_responses=True,
)


redis_connect = redis.StrictRedis(
host=REDIS_CLOUD_HOST,
port=REDIS_CLOUD_PORT,
password=REDIS_CLOUD_PASSWORD,
decode_responses=True,
)
