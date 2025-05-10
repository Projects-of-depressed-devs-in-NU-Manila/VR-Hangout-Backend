from app.routes.api.auth.request_models.signup import SignupBody 
from app.services.auth.auth import AuthService
from app.services.account.account import PlayerService
from app.services.world.worlds import WorldService
from app.core.exceptions import catch_exceptions

from fastapi import APIRouter, HTTPException
import traceback


router = APIRouter(prefix="/auth", tags=["Authentication", "Account Creation"])

@router.post("/signup")
@catch_exceptions()
async def signup(request: SignupBody):
    print(f"Creating a new account for {request.username}")
    player_id = PlayerService.create_account()
    print(f"Adding credentials...")
    AuthService.create_credentials(player_id, request.username, request.password)
    print(f"Creating default world...")
    world_id = WorldService.create_default_world(player_id)
    print(f"Successfully created user: {player_id}")
    print(f"User world: {world_id}")
