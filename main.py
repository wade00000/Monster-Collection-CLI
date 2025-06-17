from game.cli import run_game_cli
from game.database import Session

# This is the entry point for the CLI
if __name__ == "__main__":
    session = Session()
    run_game_cli(session)
