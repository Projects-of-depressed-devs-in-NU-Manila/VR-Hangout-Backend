from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel

from app.core.exceptions import DoesNotExists, catch_exceptions
from app.database.session import create_postgres_session
from app.services.inventory.inventory import InventoryService

router = APIRouter(prefix="/inventory")

class InventoryRequest(BaseModel):
    player_id: str
    object_id: str  
    qty: int = 1

@router.post("/")
@catch_exceptions()
async def add_items_to_inventory(request: InventoryRequest = Body(...)):
    try:
        with create_postgres_session() as session:
            inventory = InventoryService.add(session, request.player_id, request.object_id, request.qty)
            session.commit()
            return {"new_inventory": inventory.to_dict()} 
    except DoesNotExists as e:
        raise HTTPException(404, {"error", str(e)})

@router.get("/")
@catch_exceptions()
async def get_player_inventory(player_id: str = Query(None)):
    try:
        with create_postgres_session() as session:
            inventories = InventoryService.get(session, player_id)
            return inventories
    except DoesNotExists as e:
        raise HTTPException(404, {"error", str(e)})

@router.delete("/")
@catch_exceptions()
async def remove_items_from_inventory(request: InventoryRequest = Body(...)):
    try:
        with create_postgres_session() as session:
            inventory = InventoryService.remove(session, request.player_id, request.object_id, request.qty)
            session.commit()
            if inventory is None:
                return {"new_inventory": {}}
            return {"new_inventory": inventory.to_dict()} 
    except DoesNotExists as e:
        raise HTTPException(404, {"error", e})

