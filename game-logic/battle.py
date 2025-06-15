from models.battle import Battle, create_battle, log_battle_result, calculate_battle_rewards
from sqlalchemy.orm import Session
import random
from datetime import datetime

# Simulated battle turn between two monsters
def execute_turn(attacker, defender, move):
    move_power = move['power']
    effectiveness = move.get('effectiveness', 1.0)
    damage = calculate_damage(attacker['stats'], defender['stats'], move_power, effectiveness)
    defender['hp'] -= damage
    return {
        'attacker': attacker['name'],
        'defender': defender['name'],
        'move': move['name'],
        'damage': damage,
        'defender_remaining_hp': max(defender['hp'], 0)
    }

def calculate_damage(attacker_stats, defender_stats, power, multiplier):
    attack = attacker_stats.get('attack', 10)
    defense = defender_stats.get('defense', 5)
    damage = ((attack / defense) * power) * multiplier
    return max(1, int(damage))

# Create and simulate full AI battle
def battle_vs_ai(session: Session, player, player_monsters):
    ai = create_ai_opponent(player.level)
    ai_monsters = ai['monsters']

    battle = create_battle(session, player.id, None)

    print(f"\n⚔️  {player.name} vs {ai['username']} ⚔️\n")
    for i in range(min(len(player_monsters), len(ai_monsters))):
        player_mon = player_monsters[i]
        ai_mon = ai_monsters[i]
        turn = 1
        print(f"\n{player_mon['name']} vs {ai_mon['name']}")
        while player_mon['hp'] > 0 and ai_mon['hp'] > 0:
            print(f"\n-- Turn {turn} --")
            move = {"name": "Tackle", "power": 15, "effectiveness": 1.0}
            result = execute_turn(player_mon, ai_mon, move)
            print(f"{result['attacker']} used {result['move']}! {result['defender']} took {result['damage']} damage.")

            if ai_mon['hp'] <= 0:
                print(f"{ai_mon['name']} fainted!")
                break

            counter = execute_turn(ai_mon, player_mon, move)
            print(f"{counter['attacker']} used {counter['move']}! {counter['defender']} took {counter['damage']} damage.")

            if player_mon['hp'] <= 0:
                print(f"{player_mon['name']} fainted!")
                break
            turn += 1

    player_wins = sum(1 for m in ai_monsters if m['hp'] <= 0) > sum(1 for m in player_monsters if m['hp'] <= 0)
    result_text = "Victory!" if player_wins else "Defeat..."
    print(f"\nBattle Result: {result_text}\n")

    winner_id = player.id if player_wins else None
    log_battle_result(session, battle.id, winner_id, result_text)

    xp, gold = calculate_battle_rewards(player.id, difficulty_level=1)
    print(f"You earned {xp} XP and ${gold} for this battle!")
    return player_wins

# Simple AI opponent generator
def create_ai_opponent(level):
    return {
        "username": random.choice(["VoltBot", "TrainerAI", "OmegaMon"]),
        "monsters": [
            {"name": f"Bot-{i}", "hp": 40 + 5*i, "stats": {"attack": 12, "defense": 8}} for i in range(1, 4)
        ]
    }