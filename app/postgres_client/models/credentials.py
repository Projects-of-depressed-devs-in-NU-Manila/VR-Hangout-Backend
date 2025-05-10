from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.postgres_client.session import Base, engine


class Credential(Base):
    __tablename__= "credentials"

    credential_id = Column(String(10), primary_key=True, index=True, nullable=False)
    player_id = Column(String(10), ForeignKey("players.player_id"), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
