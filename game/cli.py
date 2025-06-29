import sys , os
from game.game_logic.catching import catch_monster
from game.cli_helpers import get_random_species, create_player_flow, login_player_flow
from game.models import PlayerMonster, MonsterSpecies, Player
from game.game_logic.battle import resolve_battle_wild_monster, resolve_battle_player
from game.game_logic.trade_social import resolve_trade_monsters,add_friend,add_rival,show_leaderboards
from game.game_logic.battle import resolve_gym_challenge
from game.game_logic.achievements import check_and_unlock_achievements


def display_main_menu():
    print("""
========== MONSTER COLLECTOR CLI ==========
1. Create Player
2. Login
3. Explore
4. View Collection
5. Battle Wild Monster
6. Battle a Player
7. Trade Monsters
8. Gym Challenge
9. View Profile 
10.View Achievements
11.View Friends and Rivals
12.Add Friend
13.Add Rival
14.Show Leaderboard
                  
15. Exit
===========================================
""")

def handle_menu_choice(choice, session, current_player):
    if choice == '1':
        player = create_player_flow(session)
        if player:
            current_player[0] = player

    elif choice == '2':
        player = login_player_flow(session)
        if player:
            current_player[0] = player

    elif choice in ['3', '4', '5', '6', '7', '8', '9','10','11','12','13','14']:
        if not current_player[0]:
            print("❗ You need to log in first!")
            return

        if choice == '3':
            explore(session, current_player[0])
        elif choice == '4':
            view_collection(session, current_player[0])
        elif choice == '5':
            battle_wild_monster(session, current_player[0])
        elif choice == '6':
            battle_player(session, current_player[0])
        elif choice == '7':
            trade_monsters(session, current_player[0])
        elif choice == '8':
            gym_challenge(session, current_player[0])
        elif choice == '9':
            view_profile (session, current_player[0])
        elif choice == '10':
            view_achievements(session, current_player[0])
        elif choice == '11':
            view_social_circle(current_player[0])
        elif choice == '12':
            name = input("Enter the name of the friend to add: ").strip()
            add_friend(session, current_player[0], name)
        elif choice == '13':
            name = input("Enter the name of the rival to add: ").strip()
            add_rival(session, current_player[0], name)
        elif choice == '14':
            show_leaderboards(session)


    elif choice == '15':
        print("Thanks for playing!")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")

# =============== Feature Flows ===============

def explore (session, player):
    print("Exploring the wild...")
    species = get_random_species(session)
    print(f"A wild {species.name} appeared!")

    choice = input("Do you want to try catching it? (y/n): ").strip().lower()
    if choice == 'y':
        success = catch_monster(session, player.id, species.id)
        if success:
            print(f"🎉 You caught {species.name}!")
            check_and_unlock_achievements(session, player, event_type='catch', event_data=species)
        else:
            print(f"{species.name} broke free!")
    else:
        print("You let the monster go.")

def view_collection (session, player):
    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    if not player_monsters:
        print("❗You don’t have any monsters yet. Go explore!")
        return

    print(f"{player.name}'s Collection:")
    for pm in player_monsters:
        species = session.query(MonsterSpecies).filter_by(id=pm.species_id).first()
        print(f"- {pm.nickname} (Species: {species.name}, Level: {pm.level})")

def battle_wild_monster(session, player):
    print("⚔️ Battling a wild monster...")
    species = get_random_species(session)
    print(f"A wild {species.name} appeared!")
    resolve_battle_wild_monster(session, player, species)

def battle_player(session, player):
    print("⚔️ Initiating battle against another player...")
    opponent_username = input("Enter opponent's username: ").strip()
    opponent = session.query(Player).filter_by(name=opponent_username).first()
    if not opponent:
        print("❗ Opponent not found.")
        return
    resolve_battle_player(session, player, opponent)

def trade_monsters(session, player):
    print("🔄 Trading monsters...")
    resolve_trade_monsters(session, player)

def gym_challenge(session, player):
    print("🏆 Challenging the gym leader!")
    resolve_gym_challenge(session, player)

def view_profile(session, player):
    print(f"\n👤 Profile for {player.name}")
    print(f"- Level: {player.level}")
    print(f"- XP: {player.xp}")
    print("- Monsters caught: ", session.query(PlayerMonster).filter_by(player_id=player.id).count())

def view_achievements( player):
    print(f"🎖️ Achievements for {player.name}:")
    player_achievements = player.achievements  

    if not player_achievements:
        print("❗ No achievements unlocked yet. Go catch some monsters or win battles!")
        return

    for pa in player_achievements:
        print(f"✅ {pa.achievement.achievement_name}: {pa.achievement.description}")

def view_social_circle(player: Player):
    print("👥 Friends:")
    if player.friends:
        for f in player.friends:
            print(f" - {f.name}")
    else:
            print("You have no friends yet try adding some")

    print("⚔️ Rivals:")
    if player.rivals:
        for r in player.rivals:
            print(f" - {r.name}")
    else:
            print("You have no rivals yet,seems you're really likable!")




def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_game_cli(session):
    current_player = [None]

    while True:
        clear_screen()
        display_main_menu()
        choice = input("Enter your choice: ").strip()
        clear_screen() # clears the terminal so you can be able to focus on output

        handle_menu_choice(choice, session, current_player)

        if choice == '15':  # Exit selected
            print("Thanks for playing Monster Collector CLI! 👋")
            break

        input("\nPress Enter to return to the main menu...")
