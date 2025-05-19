from app.database.session import engine, Base
import app.models.models

def init():
    Base.metadata.create_all(bind=engine)

