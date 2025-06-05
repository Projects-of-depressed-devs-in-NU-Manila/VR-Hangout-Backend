
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from app.database.session import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(String(10), primary_key=True, unique=True, nullable=False)
    player_id = Column(String(10), ForeignKey("players.player_id"), nullable=False)
    object_id = Column(String(100), nullable=False)
    qty = Column(Integer(), nullable=False, default=1)
    __table_args__ = (UniqueConstraint("player_id", "object_id", name="uix_player_object"),)

    def to_dict(self):
        return {
            "inventory_id": self.inventory_id,
            "player_id": self.player_id,
            "object_id": self.object_id,
            "qty": self.qty,
        }