from fastapi import APIRouter, Body, Query, HTTPException
from pydantic import BaseModel
from app.core.exceptions import AlreadyExists, DoesNotExists, catch_exceptions
from app.database.session import create_postgres_session
from app.services.friendship.friendship import FriendshipService

router = APIRouter(prefix="/friendship")

class FriendRequest(BaseModel):
    player_id1: str
    player_id2: str


@router.post("/")
@catch_exceptions()
async def add_friend(request: FriendRequest = Body(...)):
    try:
        with create_postgres_session() as session:
            friendship = FriendshipService.add_friend(session, request.player_id1, request.player_id2)

            session.commit()
            return friendship
    except DoesNotExists as e:
        raise HTTPException(404, {"error": e})
    except AlreadyExists as e:
        raise HTTPException(404, {"error": e})

@router.get("/")
@catch_exceptions()
async def get_friend_list(player_id: str = Query(None)):
    if player_id is None:
        raise HTTPException(422, {'error', "Player if must be provided"})
    
    with create_postgres_session() as session:
        friendships = FriendshipService.get_friends(session, player_id)
        return [friendship.player_id2 for friendship in friendships] 

@router.delete("/")
@catch_exceptions()
async def remove_friend(request: FriendRequest = Body(...)):
    try:
        with create_postgres_session() as session:
            FriendshipService.remove_friend(session, request.player_id1, request.player_id2)
            session.commit()

    except DoesNotExists as e:
        raise HTTPException(404, {"error": e})