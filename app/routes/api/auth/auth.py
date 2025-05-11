from app.routes.api.auth.request_models.signup import SignupBody 
from app.services.auth.auth import AuthService
from app.services.account.account import PlayerService
from app.services.world.worlds import WorldService
from app.core.exceptions import catch_exceptions, AlreadyExists

from fastapi import APIRouter, HTTPException

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
            AuthService.create_credentials(session, player_id, request.username, request.password)
            print(f"Creating default world...")
            world_id = WorldService.create_default_world(session, player_id)
            print(f"Successfully created user: {player_id}")
            print(f"User world: {world_id}")

            session.commit()
            return {"message": "Successfully registered user"}
    except AlreadyExists as e:
        raise HTTPException(409, {"detail": str(e)})
