from app.database.session import Base, engine
from sqlalchemy import Column, String, ForeignKey

class Friendship(Base):
    __tablename__ = "friendships"

    friendship_id = Column(String(10), primary_key=True, index=True, nullable=False, unique=True)
    player_id1 = Column(String(10), ForeignKey("players.player_id"),nullable=False)
    player_id2 = Column(String(10), ForeignKey("players.player_id"),nullable=False)
