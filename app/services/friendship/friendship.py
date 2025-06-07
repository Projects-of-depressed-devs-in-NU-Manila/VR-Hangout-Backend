from sqlalchemy.orm import Session
from app.core.exceptions import AlreadyExists, DoesNotExists
from app.core.id_gen import generate_id
from app.models.credentials import Credential
from app.models.friends import Friendship
from app.models.players import Player

class FriendshipService():

    @staticmethod
    def add_friend(session: Session, player_id1: str, player_id2: str):
        player1 = session.query(Player).filter(Player.player_id == player_id1).first()
        player2 = session.query(Player).filter(Player.player_id == player_id2).first()
        if player1 is None or player2 is None:
            raise DoesNotExists("Player does not exists")

        if session.query(Friendship).filter(Friendship.player_id1 == player_id1).filter(Friendship.player_id2 == player_id2).first() is not None:
            raise AlreadyExists("Already friends")

        id = generate_id(Friendship, Friendship.friendship_id)
        id2 = generate_id(Friendship, Friendship.friendship_id)
        friendship = Friendship(friendship_id=id, player_id1=player_id1, player_id2=player_id2)
        friendship2 = Friendship(friendship_id=id2, player_id1=player_id2, player_id2=player_id1)
        session.add(friendship)
        session.add(friendship2)
        return friendship

    @staticmethod
    def get_friends(session: Session, player_id: str):
        friends = session.query(Friendship).filter(Friendship.player_id1 == player_id).all()
        friends = session.query(Credential).filter(Credential.player_id.in_([friend.player_id2 for friend in friends])).all()

        return friends
     
    @staticmethod
    def remove_friend(session: Session, player_id1: str, player_id2: str):
        friendship1 = session.query(Friendship).filter(Friendship.player_id1 == player_id1).filter(Friendship.player_id2 == player_id2).first()
        if friendship1 is None:
            raise DoesNotExists("Friendship does not exist")

        friendship2 = session.query(Friendship).filter(Friendship.player_id1 == player_id2).filter(Friendship.player_id2 == player_id1).first()
        if friendship2 is None:
            raise DoesNotExists("Friendship does not exist")

        session.delete(friendship1) 
        session.delete(friendship2)
