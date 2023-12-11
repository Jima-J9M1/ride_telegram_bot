import redis

API = "A4q6itr4w49cnzuzjupze2u746o3ri3okzjkyte7gvfixvme5ge"
REDIS_CLOUD_HOST = "redis-10109.c326.us-east-1-3.ec2.cloud.redislabs.com"
REDIS_CLOUD_PORT = 10109
REDIS_CLOUD_PASSWORD = "QKZbSk6kNhXIlLUs66oqpjGBDMrYlIV4"

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
