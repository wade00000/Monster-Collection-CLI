from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from game.models import Player, PlayerMonster, Trade, MonsterSpecies, Battle


# --- TRADE SYSTEM ---

def propose_trade(session: Session, sender_id: int, receiver_id: int, monster_sent_id: int) -> Trade:
    """
    Creates and commits a trade proposal from one player to another.
    """
    trade = Trade(
        sender_id=sender_id,
        receiver_id=receiver_id,
        monster_sent=monster_sent_id,
        created_at=datetime.utcnow()
    )
    session.add(trade)
    session.commit()
    print(f"Trade proposed from Player {sender_id} to Player {receiver_id} for Monster {monster_sent_id}.")
    return trade


def accept_trade(session: Session, trade_id: int):
    """
    Accepts a trade by transferring the monster to the receiver and deleting the trade.
    """
    trade = session.query(Trade).get(trade_id)
    if not trade:
        print("Trade not found.")
        return None

    sender = session.query(Player).get(trade.sender_id)
    receiver = session.query(Player).get(trade.receiver_id)
    monster = session.query(PlayerMonster).get(trade.monster_sent)

    if monster.owner.id != sender.id:
        print("Sender does not own the monster anymore.")
        return None

    monster.owner = receiver
    session.delete(trade)
    session.commit()
    print(f"Trade accepted! Monster {monster.id} now belongs to Player {receiver.id}.")
    return monster


def resolve_trade_monsters(session: Session, player: Player):
    """
    Handles the CLI flow for initiating a monster trade with another player.
    """
    target_username = input("Enter the username of the player you want to trade with: ").strip()
    target_player = session.query(Player).filter_by(name=target_username).first()
    if not target_player:
        print("❗ Player not found.")
        return

    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    if not player_monsters:
        print("❗ You don’t have any monsters to trade!")
        return

    print("\nYour Monsters:")
    for idx, pm in enumerate(player_monsters, 1):
        species = session.query(MonsterSpecies).filter_by(id=pm.species_id).first()
        print(f"{idx}. {pm.nickname} (Species: {species.name}, Level: {pm.level})")

    try:
        choice = int(input("Enter the number of the monster you want to trade: "))
        selected_monster = player_monsters[choice - 1]
    except (ValueError, IndexError):
        print("❗ Invalid choice.")
        return

    selected_monster.player_id = target_player.id
    session.commit()
    print(f"🔄 Traded {selected_monster.nickname} to {target_player.name}!")


# --- SOCIAL SYSTEM ---

def add_friend(session: Session, player: Player, friend_name: str):
    """
    Adds another player as a friend if not already added.
    """
    friend = session.query(Player).filter_by(name=friend_name).first()

    if not friend:
        print("❗ No such player found.")
        return
    if player.id == friend.id:
        print("❗ You can’t be your own friend.")
        return
    if friend in player.friends:
        print(f"✅ {friend.name} is already your friend.")
        return

    player.friends.append(friend)
    session.commit()
    print(f"👯 {friend.name} added as a friend!")


def add_rival(session: Session, player: Player, rival_name: str):
    """
    Adds another player as a rival if not already marked as one.
    """
    rival = session.query(Player).filter_by(name=rival_name).first()

    if not rival:
        print("❗ No such player found.")
        return
    if player.id == rival.id:
        print("❗ You can’t be your own rival.")
        return
    if rival in player.rivals:
        print(f"⚔️ {rival.name} is already your rival.")
        return

    player.rivals.append(rival)
    session.commit()
    print(f"💢 {rival.name} added as a rival!")


# --- LEADERBOARDS ---

def get_battle_wins_leaderboard(session: Session, limit: int = 10):
    """
    Returns top players by number of battle wins.
    """
    return (
        session.query(
            Player.name,
            func.count(Battle.id).label("wins")
        )
        .join(Battle, Battle.winner_id == Player.id)
        .group_by(Player.id)
        .order_by(func.count(Battle.id).desc())
        .limit(limit)
        .all()
    )


def get_collection_leaderboard(session: Session, limit: int = 10):
    """
    Returns top players by the size of their monster collection.
    """
    return (
        session.query(
            Player.name,
            func.count(PlayerMonster.id).label("collection_size")
        )
        .join(PlayerMonster, Player.id == PlayerMonster.player_id)
        .group_by(Player.id)
        .order_by(func.count(PlayerMonster.id).desc())
        .limit(limit)
        .all()
    )


def show_leaderboards(session: Session):
    """
    Displays the top players for wins and collections to the CLI.
    """
    print("\n🏆 Battle Wins Leaderboard:")
    for i, (username, wins) in enumerate(get_battle_wins_leaderboard(session), 1):
        print(f"{i}. {username} - {wins} wins")

    print("\n🐾 Monster Collection Leaderboard:")
    for i, (username, collection_size) in enumerate(get_collection_leaderboard(session), 1):
        print(f"{i}. {username} - {collection_size} monsters")

    input("\nPress Enter to return to the main menu...")
