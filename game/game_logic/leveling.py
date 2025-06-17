from game.models import Player, PlayerMonster

def level_up_monster(session, player_monster_id) -> dict:
    """
    Force level-up for a monster (bypasses XP).
    
    """
    monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not monster:
        return {"success": False, "error": "Monster not found."}

    monster.level += 1
    calculate_stats(session, monster.id)
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
    """
    Recalculate and update monster stats based on level.
    
    """
    monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not monster:
        return {"error": "Monster not found."}

    level = monster.level
    base_stats = monster.species.base_stats

    updated_stats = {}
    for stat_name, base_value in base_stats.items():
        if stat_name == "hp":
            value = ((base_value * 2 * level) // 100) + level + 10
        else:
            value = ((base_value * 2 * level) // 100) + 5
        updated_stats[stat_name] = value

    monster.current_stats = updated_stats
    session.add(monster)
    session.commit()

    return updated_stats

def xp_to_next_monster_level(level: int) -> int:
    """
    XP required for a monster to reach the next level.
    
    """
    return int(50 * (1.2 ** (level - 1)))

def add_xp_to_monster(session, player_monster_id, xp_amount) -> dict:
    """
    Add XP to a monster, handling level-ups and stat recalculation.
    
    """
    monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not monster:
        return {"error": "Monster not found."}

    monster.xp += xp_amount
    leveled_up = False

    while monster.xp >= xp_to_next_monster_level(monster.level):
        monster.xp -= xp_to_next_monster_level(monster.level)
        monster.level += 1
        calculate_stats(session, monster.id)
        leveled_up = True

    session.commit()

    return {
        "id": monster.id,
        "nickname": monster.nickname,
        "level": monster.level,
        "xp": monster.xp,
        "leveled_up": leveled_up,
        "current_stats": monster.current_stats,
    }

def xp_to_next_player_level(level: int) -> int:
    """
    XP required for a player to reach the next level.
    """
    return int(100 * (1.3 ** (level - 1)))

def add_xp_to_player(session, player_id, xp_amount) -> dict:
    """
    Add XP to a player, handling level-ups.
    """
    player = session.query(Player).filter_by(id=player_id).first()
    if not player:
        return {"error": "Player not found."}

    player.xp += xp_amount
    leveled_up = False

    while player.xp >= xp_to_next_player_level(player.level):
        player.xp -= xp_to_next_player_level(player.level)
        player.level += 1
        leveled_up = True

    session.commit()

    return {
        "id": player.id,
        "username": player.name,
        "level": player.level,
        "xp": player.xp,
        "money": player.money,
        "leveled_up": leveled_up
    }
