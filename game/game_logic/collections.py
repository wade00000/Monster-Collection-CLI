from game.models import PlayerMonster

def get_player_collection(session, player_id: int) -> list:
    """
    Retrieves all monsters belonging to a player and returns them as a list of dictionaries.
    """
    collection = (
        session.query(PlayerMonster)
        .filter_by(player_id=player_id)
        .all()
    )
    return [
        {
            "id": monster.id,
            "nickname": monster.nickname,
            "species_name": monster.species.name,
            "level": monster.level
        }
        for monster in collection
    ]
 
def rename_monster(session, player_monster_id, new_name) -> dict:
    """
    Renames a player's monster if it exists and the new name is valid.
    """
    monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not monster:
        return {"error": "Monster not found."}
    
    if new_name:
        monster.nickname = new_name
    else:
        return "new name cannot be empty" 
    
    session.commit()

    return {
        "id": monster.id,
        "nickname": monster.nickname,
        "species_name": monster.species.name,
        "level": monster.level
    }

def release_monster(session, player_monster_id) -> dict:
    """
    Deletes a monster from the player's collection if found.
    """
    monster = session.query(PlayerMonster).filter_by(id=player_monster_id).first()
    if not monster:
        return {"success": False, "error": "Monster not found."}
    
    session.delete(monster)
    session.commit()
    return {"success": True, "message": f"Released monster ID {player_monster_id}"}
