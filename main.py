from database import init_db, Session
from models import Player

def run():
    init_db()
    session = Session()
    name = input("Enter player name: ")
    player = Player(name=name)
    session.add(player)
    session.commit()
    session.close()

if __name__ == "__main__":
    run()
