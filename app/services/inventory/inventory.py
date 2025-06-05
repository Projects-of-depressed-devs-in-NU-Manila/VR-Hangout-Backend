
from sqlalchemy.orm import Session

from app.core.exceptions import DoesNotExists
from app.core.id_gen import generate_id
from app.models.inventory import Inventory
from app.models.players import Player

class InventoryService():
    @staticmethod
    def add(session: Session, player_id: str, object_id: str, qty: int = 1):
        player_exists = session.query(Player).filter(Player.player_id == player_id).first()
        if not player_exists:
            raise DoesNotExists("Player does not exist")

        inventory = session.query(Inventory).filter(Inventory.player_id == player_id).filter(Inventory.object_id == object_id).first()
        if inventory is not None:
            inventory.qty += qty #type: ignore
            return inventory

        id = generate_id(Inventory, Inventory.inventory_id)
        inventory = Inventory(inventory_id=id, player_id=player_id, object_id=object_id, qty=qty)
        session.add(inventory)
        return inventory
    
    @staticmethod
    def get(session: Session, player_id):
        player_exists = session.query(Player).filter(Player.player_id == player_id).first()
        if not player_exists:
            raise DoesNotExists("Player does not exist")

        inventories = session.query(Inventory).filter(Inventory.player_id == player_id).all()
        return inventories
    
    @staticmethod
    def remove(session: Session, player_id: str, object_id: str, qty:int):
        player_exists = session.query(Player).filter(Player.player_id == player_id).first()
        if not player_exists:
            raise DoesNotExists("Player does not exist")

        inventory = session.query(Inventory).filter(Inventory.player_id == player_id).filter(Inventory.object_id == object_id).first()
        if inventory is None:
            raise DoesNotExists("Player does not have that item")
        
        inventory.qty -= qty #type: ignore

        if inventory.qty <= 0: #type: ignore
            session.delete(inventory)
            return None
        return inventory


