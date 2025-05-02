from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import traceback

from config import database_connection_string

engine = create_engine(database_connection_string)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# dont forget to close this or use with "with" statement
def create_postgres_session() -> Session:
    db: Session = SessionLocal()
    try: 
        return db
    except Exception as e:
        print("ERROR ESRABLISHING CONNECTION TO DATABSE")
        print(traceback.format_exc())
