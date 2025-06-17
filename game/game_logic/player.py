from game.models import Player

def create_player(session, name):
    """
    Creates a new player if the username is not already taken.
    """
    existing = session.query(Player).filter_by(name=name).first()
    if existing:
        print(f"username: '{name}' already taken.")
        return None

    new_player = Player(name=name)
    session.add(new_player)
    session.commit()
    print(f"Player '{name}' created!")
    return new_player

def login_player(session, name):
    """
    Logs in a player by name if they exist in the database.
    """
    player = session.query(Player).filter_by(name=name).first()
    if player:
        print(f"Welcome back, {name}!")
        return player
    print("Player not found.")
    return None

def view_player_profile(player):
    """
    Displays the player’s profile, including stats and unlocked achievements.
    """
    print(f"\n👤 Player Profile: {player.name}")
    print(f"Level: {player.level}")
    print(f"Experience: {player.experience}/{player.level * 100}")
    print(f"Money: ${player.money}")
    print("Achievements:")
    for pa in player.achievements:
        print(f"🏅 {pa.achievement.name} - {pa.achievement.description}")
