from models import PlayerMonster

def level_up_monster(session,player_monster_id) -> dict:
    monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not monster:
        return {"success": False, "error": "Monster not found."}

    monster.level += 1
    session.commit()

    return {
        "success": True,
        "message": f"{monster.nickname or monster.species.name} leveled up to {monster.level}!",
        "data": {
            "id": monster.id,
            "nickname": monster.nickname,
            "level": monster.level
        }
    }

def calculate_stats(session, player_monster_id) -> dict:
    player_monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not player_monster:
        return {"error": "Monster not found."}

    level = player_monster.level
    base_stats = player_monster.species.base_stats  

    updated_stats = {}
    for stat_name, base_value in base_stats.items():
        if stat_name == "hp":
            value = ((base_value * 2 * level) // 100) + level + 10
        else:
            value = ((base_value * 2 * level) // 100) + 5
        updated_stats[stat_name] = value

    player_monster.current_stats = updated_stats  
    session.add(player_monster)
    session.commit()

    return updated_stats

def xp_to_next_level(level: int) -> int:
    return int(50 * (1.2 ** (level - 1)))  # Level 1: 50 XP, Level 5: ~120 XP

def add_xp(session, player_monster_id, xp_amount)-> dict:
    player_monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not player_monster:
        return {"error": "Monster not found."}
    
    player_monster.xp += xp_amount
    leveled_up = False
    
    while player_monster.xp >= xp_to_next_level(player_monster.level):
        player_monster.xp -= xp_to_next_level(player_monster.level)
        player_monster.level += 1
        calculate_stats(session, player_monster.id)  # Recalculate stats
        leveled_up = True

    session.commit()

    return {
        "id": player_monster.id,
        "nickname": player_monster.nickname,
        "level": player_monster.level,
        "xp": player_monster.xp,
        "leveled_up": leveled_up,
        "current_stats": player_monster.current_stats,
    }
    