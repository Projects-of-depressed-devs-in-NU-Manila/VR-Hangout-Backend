import config
import postgres_client.session
from redis_client.session import create_redis_session

if config.initializa_db_on_run:
    from postgres_client.init import init
    print("Initialize database on run is true. Initializing database tables")
    init()
    print("Database table initialization sequence done!")






