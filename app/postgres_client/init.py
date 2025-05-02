from postgres_client.session import engine, Base
#import models

def init():
    Base.metadata.create_all(bind=engine)