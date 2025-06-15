from sqlalchemy.orm import Session
from game.models import PlayerMonster, MonsterSpecies, Player
import random

def calculate_catch_rate(species_rarity, player_level) -> float:
    base_rates = {
        "Common": 0.9,
        "Uncommon": 0.7,
        "Rare": 0.5,
        "Legendary": 0.2,
    }
    base_rate = base_rates.get(species_rarity, 0.5)
    return min(1.0, base_rate + (player_level * 0.01))  # Cap at 1.0/100% so it doesnt go higher

def catch_monster(session: Session, player_id: int, species_id: int) -> bool:
    species = session.query(MonsterSpecies).filter_by(id=species_id).first()
    player = session.query(Player).filter_by(id=player_id).first()
    if not species or not player:
        return False

    catch_chance = calculate_catch_rate(species.rarity, player.level) 
    if random.random() <= catch_chance:
        new_monster = PlayerMonster(
            player_id=player_id, 
            species_id=species_id, 
            nickname=species.name, 
            level=1,
            current_stats=species.base_stats  # Important cause levelling broke at some point without it 💀
            )
        
        session.add(new_monster)
        session.commit()
        return True
    return False
