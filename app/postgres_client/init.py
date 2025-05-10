from app.postgres_client.session import engine, Base
import app.postgres_client.models.models

def init():
    Base.metadata.create_all(bind=engine)

