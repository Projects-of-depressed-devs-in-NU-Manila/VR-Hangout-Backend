from redis_om import get_redis_connection

redis = get_redis_connection(
    host='localhost',
    port=6379,
    decode_responses=True
)


def get_redis_session():
    return redis
