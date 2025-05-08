from redis import Redis, ConnectionPool

r = Redis(host="localhost", port=6379)

def create_redis_session() -> Redis:
    return r  
