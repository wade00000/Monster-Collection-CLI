import random
from game.models import Battle, TypeEffectiveness,PlayerMonster,MonsterSpecies
from sqlalchemy.orm import Session
from game.game_logic.leveling import add_xp_to_monster
from datetime import datetime

def create_battle(session, player1_id, player2_id, monster_teams=None):
    battle = Battle(player1_id=player1_id, player2_id=player2_id)
    session.add(battle)
    session.commit()
    return {
        "battle_id": battle.id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "created_at": battle.created_at
    }

# ====================
# Utility: Type Multiplier
# ====================
def get_type_multiplier(session, attacker_type_id, defender_type_id):
    effectiveness = session.query(TypeEffectiveness).filter_by(
        attacking_type_id=attacker_type_id,
        defending_type_id=defender_type_id
    ).first()
    return effectiveness.multiplier if effectiveness else 1.0

# ====================
# Damage Calculation
# ====================
def calculate_damage(attacker_stats, defender_stats, power, multiplier):
    attack = attacker_stats.get("attack", 10)
    defense = defender_stats.get("defense", 5)
    damage = ((attack / defense) * power) * multiplier
    return max(1, int(damage))

def calculate_battle_rewards(winner_id,battle_difficulty) -> tuple:
    """
    Returns tuple: (xp_reward, money_reward)
    """
    base_xp = 100
    base_money = 50
    xp = base_xp * battle_difficulty
    money = base_money * battle_difficulty
    return (xp, money)

# ====================
# Execute Single Turn
# ====================
def execute_turn(session, attacker, defender, move):
    multiplier = get_type_multiplier(session, attacker.species.type_id, defender.species.type_id)
    damage = calculate_damage(attacker.current_stats, defender.current_stats, move["power"], multiplier)
    
    defender.current_hp = max(defender.current_hp - damage, 0)
    session.add(defender)
    session.commit()

    return {
        "attacker": attacker.nickname or attacker.species.name,
        "defender": defender.nickname or defender.species.name,
        "move": move["name"],
        "damage": damage,
        "defender_remaining_hp": defender.current_hp
    }

# ====================
# Generate AI Opponent (Improved)
# ====================
def create_ai_opponent(level):
    return [
        {
            "name": f"Bot-{i}",
            "hp": 40 + 5 * i,
            "stats": {"attack": 12, "defense": 8}
        }
        for i in range(1, 4)
    ]

# ====================
# Battle Simulation vs AI
# ====================
def battle_vs_ai(session: Session, player, player_monsters):
    moves = [
        {"name": "Tackle", "power": 15},
        {"name": "Bite", "power": 20},
        {"name": "Quick Attack", "power": 12},
    ]

    ai_monsters = create_ai_opponent(player.level)

    # Create battle record
    battle = Battle(player1_id=player.id, created_at=datetime.utcnow())
    session.add(battle)
    session.commit()

    print(f"\n⚔️  {player. name} vs AI ⚔️\n")

    player_wins = 0
    ai_wins = 0

    for i in range(min(len(player_monsters), len(ai_monsters))):
        player_mon = player_monsters[i]
        ai_mon = ai_monsters[i]

        # Reset player monster HP to full for battle
        player_mon.current_hp = player_mon.current_stats["hp"]
        session.add(player_mon)
        session.commit()

        ai_hp = ai_mon["hp"]
        turn = 1

        print(f"\n{player_mon.nickname or player_mon.species.name} vs {ai_mon['name']}")

        while player_mon.current_hp > 0 and ai_hp > 0:
            print(f"\n-- Turn {turn} --")

            # Player attacks AI
            move = random.choice(moves)
            damage = calculate_damage(player_mon.current_stats, ai_mon["stats"], move["power"], 1.0)
            ai_hp = max(ai_hp - damage, 0)
            print(f"{player_mon.nickname or player_mon.species.name} used {move['name']}! {ai_mon['name']} took {damage} damage.")

            if ai_hp <= 0:
                print(f"{ai_mon['name']} fainted!")
                player_wins += 1
                break

            # AI attacks Player
            counter_move = random.choice(moves)
            counter_damage = calculate_damage(ai_mon["stats"], player_mon.current_stats, counter_move["power"], 1.0)
            player_mon.current_hp = max(player_mon.current_hp - counter_damage, 0)
            session.add(player_mon)
            session.commit()
            print(f"{ai_mon['name']} used {counter_move['name']}! {player_mon.nickname or player_mon.species.name} took {counter_damage} damage.")

            if player_mon.current_hp <= 0:
                print(f"{player_mon.nickname or player_mon.species.name} fainted!")
                ai_wins += 1
                break
            turn += 1

    # Determine result
    player_won_battle = player_wins > ai_wins
    result_text = "Victory!" if player_won_battle else "Defeat..."
    print(f"\nBattle Result: {result_text}")

    # Log battle result
    winner_id = player.id if player_won_battle else None
    battle.result = result_text
    battle.winner_id = winner_id
    session.add(battle)
    session.commit()

    # Rewards and XP
    if player_won_battle:
        xp, gold = calculate_battle_rewards(player.id, difficulty_level=1)
        split_xp = xp // len(player_monsters)
        for player_mon in player_monsters:
            add_xp_to_monster(session, player_mon.id, split_xp)
        player.money += gold
        session.add(player)
        session.commit()
        print(f"You earned {xp} XP and ${gold}!")

    return player_won_battle



def resolve_battle_wild_monster(session, player, species):
    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    if not player_monsters:
        print("❗ You don’t have any monsters yet. Go catch one first!")
        return

    player_monster = random.choice(player_monsters)
    print(f"⚔️ {player_monster.nickname} (Lv {player_monster.level}) vs {species.name} (Lv {species.base_level})!")

    player_power = player_monster.level + random.randint(0, 5)
    wild_power = species.base_level + random.randint(0, 5)

    if player_power >= wild_power:
        print(f"🏆 {player_monster.nickname} defeated the wild {species.name}!")
        player.xp += 10
        session.commit()
    else:
        print(f"❗ The wild {species.name} defeated your {player_monster.nickname}!")


def resolve_battle_player(session, player, opponent):
    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    opponent_monsters = session.query(PlayerMonster).filter_by(player_id=opponent.id).all()

    if not player_monsters:
        print("❗ You don’t have any monsters! Go explore first.")
        return
    if not opponent_monsters:
        print("❗ Opponent doesn’t have any monsters!")
        return

    player_monster = random.choice(player_monsters)
    opponent_monster = random.choice(opponent_monsters)

    print(f"⚔️ {player. name}'s {player_monster.nickname} (Lv {player_monster.level}) vs {opponent. name}'s {opponent_monster.nickname} (Lv {opponent_monster.level})!")

    player_power = player_monster.level + random.randint(0, 5)
    opponent_power = opponent_monster.level + random.randint(0, 5)

    if player_power >= opponent_power:
        print(f"🏆 {player. name} wins!")
        player.xp += 20
        session.commit()
    else:
        print(f"❗ {opponent. name} wins!")


def resolve_battle_player(session, player, opponent):
    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    opponent_monsters = session.query(PlayerMonster).filter_by(player_id=opponent.id).all()

    if not player_monsters:
        print("❗ You don’t have any monsters! Go explore first.")
        return
    if not opponent_monsters:
        print("❗ Opponent doesn’t have any monsters!")
        return

    player_monster = random.choice(player_monsters)
    opponent_monster = random.choice(opponent_monsters)

    print(f"⚔️ {player. name}'s {player_monster.nickname} (Lv {player_monster.level}) vs {opponent. name}'s {opponent_monster.nickname} (Lv {opponent_monster.level})!")

    player_power = player_monster.level + random.randint(0, 5)
    opponent_power = opponent_monster.level + random.randint(0, 5)

    if player_power >= opponent_power:
        print(f"🏆 {player. name} wins!")
        player.xp += 20
        session.commit()
    else:
        print(f"❗ {opponent. name} wins!")


def resolve_gym_challenge(session, player):
    gym_leader_monster_level = player.level + 5
    print(f"🏟️ Gym Leader sends out a monster (Lv {gym_leader_monster_level})!")

    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    if not player_monsters:
        print("❗ You don’t have any monsters!")
        return

    player_monster = random.choice(player_monsters)
    player_power = player_monster.level + random.randint(0, 5)
    gym_power = gym_leader_monster_level + random.randint(0, 5)

    if player_power >= gym_power:
        print(f"🏆 Congratulations! You defeated the Gym Leader!")
        player.xp += 50
        session.commit()
    else:
        print(f"❗ You lost to the Gym Leader. Train harder next time!")


def check_battle_end(player_monsters, ai_monsters):
    player_alive = any(mon.current_hp > 0 for mon in player_monsters)
    ai_alive = any(mon['hp'] > 0 for mon in ai_monsters)
    return not (player_alive and ai_alive)

def apply_status_effects(monster, effect_type):
    if effect_type == "burn":
        burn_damage = int(monster.current_stats['hp'] * 0.05)
        monster.current_hp = max(monster.current_hp - burn_damage, 0)
    elif effect_type == "paralyze":
        return random.random() < 0.5  # True = skip turn

