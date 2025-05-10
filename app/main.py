import app.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.websockets import game
from app.routes.api.auth import auth 
from app.redis_client.session import redis

if app.config.initializa_db_on_run:
    from app.postgres_client.init import init
    print("Initialize database on run is true. Initializing database tables")
    init()  
    print("Database table initialization sequence done!")

# if not redis.ping():
#     print("cannot ping redi")
# else:
#     print("Successful redis ping")
redis.set("test", "hello")
  

app = FastAPI(
    title="VR Hangout",
    description="Connect all routers here",
    version="0.1"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router)
app.include_router(auth.router)

