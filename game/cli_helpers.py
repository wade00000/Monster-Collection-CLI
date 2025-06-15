import random
from game.models import MonsterSpecies
from game.models import Player
from game.game_logic.player import create_player, login_player

def get_random_species(session):
    species_list = session.query(MonsterSpecies).all()
    return random.choice(species_list)

def create_player_flow(session):
    username = input("Choose a username: ").strip()
    return create_player(session, username)

def login_player_flow(session):
    username = input("Enter your username: ").strip()
    return login_player(session, username)
