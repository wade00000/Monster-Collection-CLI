from game.models import PlayerMonster, PlayerAchievement, Achievement, Battle
from sqlalchemy.orm import Session

def check_and_unlock_achievements(session: Session, player, event_type: str, event_data=None):
    """
    Unlocks achievements for the player based on the type of event.
    """
    unlocked_conditions = {
        pa.achievement.unlock_condition
        for pa in player.achievements
    }
    
    def unlock_if_needed(condition: str):
        if condition not in unlocked_conditions:
            achievement = session.query(Achievement).filter_by(unlock_condition=condition).first()
            if achievement:
                new_unlock = PlayerAchievement(player_id=player.id, achievement_id=achievement.id)
                session.add(new_unlock)
                print(f"🎉 Achievement Unlocked: {achievement.achievement_name}")
    
    if event_type == 'catch':
        total_caught = session.query(PlayerMonster).filter_by(player_id=player.id).count()

        if total_caught >= 1:
            unlock_if_needed('catch_1')# achievement_name="First Catch", description="Catch your first monster", unlock_condition="catch_1")
        if total_caught >= 10:
            unlock_if_needed('catch_10')# achievement_name="Collector", description="Catch 10 monsters", unlock_condition="catch_10"),
        if (
            event_data and
            hasattr(event_data, "rarity") and
            event_data.rarity.lower() == 'legendary'
        ):
            unlock_if_needed('catch_legendary')# achievement_name="Legendary Hunter", description="Catch a legendary monster", unlock_condition="catch_legendary"),

    elif event_type in ['battle_win', 'battle_player', 'battle_ai']:
        
        wins = session.query(Battle).filter_by(winner_id=player.id).count()

        print(f"You have {wins} total battle wins.")

        if wins >= 1:
            unlock_if_needed('win_1')# achievement_name="Battle Novice", description="Win your first battle", unlock_condition="win_1"),
        if wins >= 50:
            unlock_if_needed('win_50')# achievement_name="Champion", description="Win 50 battles", unlock_condition="win_50"),

    session.commit()
