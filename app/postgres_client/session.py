from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import traceback

from app.config import database_connection_string

engine = create_engine(database_connection_string)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

   
from contextlib import contextmanager

@contextmanager
def create_postgres_session():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        print("ERROR ESTABLISHING CONNECTION TO DATABASE")
        print(traceback.format_exc())
        raise
    finally:
        db.close()

