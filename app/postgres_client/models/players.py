from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.postgres_client.session import Base, engine


class Player(Base):
    __tablename__= "players"

    player_id = Column(String(10), primary_key=True, index=True, nullable=False)
    

