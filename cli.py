def display_main_menu():
    print("""
========== MONSTER COLLECTOR CLI ==========
1. Start Game
2. Explore
3. View Collection
4. Battle Wild Monster
5. Battle a Player
6. Trade Monsters
7. Gym Challenge
8. View Profile
9. Exit
===========================================
""")

def handle_menu_choice(choice):
    if choice == '1':
        print("Starting new game...")
        # Handle player creation and starter selection
    elif choice == '2':
        print("Exploring the wild... (catching logic here)")
    elif choice == '3':
        print("Displaying your monster collection...")
    elif choice == '4':
        print("Initiating battle with wild monster...")
    elif choice == '5':
        print("Initiating PvP battle...")
    elif choice == '6':
        print("Starting trade system...")
    elif choice == '7':
        print("Challenging the gym leader!")
    elif choice == '8':
        print("Showing player profile & achievements...")
    elif choice == '9':
        print("Thanks for playing!")
        exit()
    else:
        print("Invalid choice. Please try again.")

def run_game_cli():
    while True:
        display_main_menu()
        choice = input("Enter your choice: ")
        handle_menu_choice(choice)

if __name__ == "__main__":
    run_game_cli()
