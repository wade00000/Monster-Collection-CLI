# app/seed.py

from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import Player, MonsterSpecies, Achievement, Type
from database import engine
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()

TYPES = ["Fire", "Water", "Grass", "Electric", "Rock", "Psychic", "Ice"]

RARITIES = ["Common", "Uncommon", "Rare", "Legendary"]

PREDEFINED_MONSTERS = [
    {"name": "Flametail", "type": "Fire", "base_stats": {"hp": 50, "attack": 60, "defense": 40, "speed": 55}, "rarity": "Common", "abilities": ["Ember", "Scratch"]},
    {"name": "Aqualing", "type": "Water", "base_stats": {"hp": 60, "attack": 50, "defense": 50, "speed": 45}, "rarity": "Common", "abilities": ["Splash", "Bubble"]},
    {"name": "Leafyra", "type": "Grass", "base_stats": {"hp": 55, "attack": 45, "defense": 60, "speed": 40}, "rarity": "Uncommon", "abilities": ["Vine Whip", "Growl"]},
    {"name": "Zaplet", "type": "Electric", "base_stats": {"hp": 40, "attack": 70, "defense": 30, "speed": 80}, "rarity": "Uncommon", "abilities": ["Spark", "Quick Attack"]},
    {"name": "Bouldroll", "type": "Rock", "base_stats": {"hp": 80, "attack": 55, "defense": 85, "speed": 20}, "rarity": "Rare", "abilities": ["Rock Throw", "Defense Curl"]},
    {"name": "Mindrake", "type": "Psychic", "base_stats": {"hp": 50, "attack": 30, "defense": 40, "speed": 70}, "rarity": "Rare", "abilities": ["Confuse", "Psybeam"]},
    {"name": "Frostrune", "type": "Ice", "base_stats": {"hp": 45, "attack": 55, "defense": 50, "speed": 60}, "rarity": "Uncommon", "abilities": ["Frost Bite", "Icy Wind"]},
    {"name": "Infernalor", "type": "Fire", "base_stats": {"hp": 70, "attack": 85, "defense": 65, "speed": 50}, "rarity": "Legendary", "abilities": ["Flame Burst", "Inferno"]},
    {"name": "Hydross", "type": "Water", "base_stats": {"hp": 80, "attack": 75, "defense": 70, "speed": 55}, "rarity": "Legendary", "abilities": ["Hydro Pump", "Whirlpool"]},
    {"name": "Thundrake", "type": "Electric", "base_stats": {"hp": 60, "attack": 80, "defense": 50, "speed": 90}, "rarity": "Rare", "abilities": ["Thunderbolt", "Charge"]},
    {"name": "Floracorn", "type": "Grass", "base_stats": {"hp": 65, "attack": 50, "defense": 60, "speed": 55}, "rarity": "Uncommon", "abilities": ["Razor Leaf", "Heal"]},
    {"name": "Cryosting", "type": "Ice", "base_stats": {"hp": 55, "attack": 65, "defense": 40, "speed": 75}, "rarity": "Rare", "abilities": ["Icicle Spear", "Freeze"]},
    {"name": "Volcarok", "type": "Rock", "base_stats": {"hp": 90, "attack": 70, "defense": 90, "speed": 25}, "rarity": "Rare", "abilities": ["Rock Slide", "Eruption"]},
    {"name": "Brainwave", "type": "Psychic", "base_stats": {"hp": 60, "attack": 35, "defense": 55, "speed": 80}, "rarity": "Rare", "abilities": ["Mind Blast", "Calm Mind"]},
    {"name": "Terradillo", "type": "Rock", "base_stats": {"hp": 75, "attack": 60, "defense": 80, "speed": 35}, "rarity": "Uncommon", "abilities": ["Rollout", "Harden"]},
]

def reset_database():
    from models import Base 
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset complete.")

def seed_types():
    for type_name in TYPES:
        type_obj = Type(name=type_name)
        session.add(type_obj)
    session.commit()

def seed_monster_species():
    for monster in PREDEFINED_MONSTERS:
        type_obj = session.query(Type).filter_by(name=monster["type"]).first()
        if not type_obj:
            raise ValueError(f"Type '{monster['type']}' not found in the database.")
        species = MonsterSpecies(
            name=monster["name"],
            type_obj=type_obj,
            base_stats=monster["base_stats"],
            rarity=monster["rarity"],
            abilities=monster["abilities"]
        )
        session.add(species)
    session.commit()

def seed_players(n):
    players = []
    for _ in range(n):
        player = Player(name=fake.unique.first_name())
        session.add(player)
        players.append(player)
    session.commit()
    return players

def seed_achievements():
    achievements = [
        Achievement(achievement_name="First Catch", description="Catch your first monster", unlock_condition="catch_1"),
        Achievement(achievement_name="Battle Novice", description="Win your first battle", unlock_condition="win_1"),
        Achievement(achievement_name="Collector", description="Catch 10 monsters", unlock_condition="catch_10"),
        Achievement(achievement_name="Champion", description="Win 50 battles", unlock_condition="win_50"),
        Achievement(achievement_name="Legendary Hunter", description="Catch a legendary monster", unlock_condition="catch_legendary"),
    ]
    session.add_all(achievements)
    session.commit()

def seed():
    reset_database()
    
    print("Seeding Types...")
    seed_types()
    
    print("Seeding Monster Species...")
    seed_monster_species()
    
    print("Seeding Players...")
    seed_players(10)
    
    print("Seeding Achievements...")
    seed_achievements()
    
    print("Database seeding complete.")

if __name__ == "__main__":
    seed()
