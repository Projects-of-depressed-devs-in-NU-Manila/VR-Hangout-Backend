from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database.session import Base, engine


class World(Base):
    __tablename__= "worlds"

    world_id = Column(String(10), primary_key=True, index=True, nullable=False, unique=True)
    owner_player_id = Column(String(10), ForeignKey("players.player_id"), nullable=False)

    
 