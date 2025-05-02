import config
import db.session
from redis_client.session import create_redis_session

if config.initializa_db_on_run:
    from db.init import init
    print("Initialize database on run is true. Initializing database tables")
    init()
    print("Database table initialization sequence done!")






