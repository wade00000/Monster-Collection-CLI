def create_player(session, username):
    from models.player import Player
    existing = session.query(Player).filter_by(username=username).first()
    if existing:
        print(f"Username '{username}' already taken.")
        return None
    new_player = Player(username=username)
    session.add(new_player)
    session.commit()
    print(f"Player '{username}' created!")
    return new_player

def login_player(session, username):
    from models.player import Player
    player = session.query(Player).filter_by(username=username).first()
    if player:
        print(f"Welcome back, {username}!")
        return player
    print("Player not found.")
    return None

def add_experience(player, amount, session):
    player.experience += amount
    level_up_threshold = 100 * player.level
    if player.experience >= level_up_threshold:
        player.level += 1
        player.experience = 0
        print(f"{player.username} leveled up! Now level {player.level} 🎉")
    session.commit()

def view_player_profile(player):
    print(f"\n👤 Player Profile: {player.username}")
    print(f"Level: {player.level}")
    print(f"Experience: {player.experience}/{player.level * 100}")
    print(f"Money: ${player.money}")
    print("Achievements:")
    for pa in player.achievements:
        print(f"🏅 {pa.achievement.name} - {pa.achievement.description}")


