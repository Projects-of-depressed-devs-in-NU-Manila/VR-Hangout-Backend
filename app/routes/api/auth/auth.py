from app.models.worlds import World
from app.routes.api.auth.request_models.signup import SignupBody 
from app.services.auth.auth import AuthService
from app.services.account.account import PlayerService
from app.services.world.worlds import WorldService
from app.core.exceptions import DoesNotExists, catch_exceptions, AlreadyExists

from fastapi import APIRouter, HTTPException, Query

from app.database.session import create_postgres_session


router = APIRouter(prefix="/auth", tags=["Authentication", "Account Creation"])

@router.post("/signup")
@catch_exceptions()
async def signup(request: SignupBody):

    try:
        with create_postgres_session() as session:
            print(f"Creating a new account for {request.username}")
            player_id = PlayerService.create_account(session)
            print(f"Adding credentials...")
            credential = AuthService.create_credentials(session, player_id, request.username, request.password)
            print(f"Creating default world...")
            world_id = WorldService.create_default_world(session, player_id)
            print(f"Successfully created user: {player_id}")
            print(f"User world: {world_id}")

            session.commit()
            return credential
    except AlreadyExists as e:
        raise HTTPException(409, {"detail": str(e)})

@router.post("/signin")
@catch_exceptions()
async def signin(request: SignupBody):
    try:
        with create_postgres_session() as session:
            credentials = AuthService.signin(session, request.username, request.password)
            return credentials
    except DoesNotExists as e:
        raise HTTPException(494, {"error", e})
    
@router.get("/world_id")
@catch_exceptions()
async def get_world_oject(player_id: str = Query(...)):
    with create_postgres_session() as session:
        world = session.query(World).filter(World.owner_player_id == player_id).one()
        return world.world_id


