from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    money = Column(Float, default=100.0)

    monsters = relationship("PlayerMonster", back_populates="owner")
    battles_as_player1 = relationship("Battle", foreign_keys="Battle.player1_id", back_populates="player1")
    battles_as_player2 = relationship("Battle", foreign_keys="Battle.player2_id", back_populates="player2")
    battles_won = relationship("Battle", foreign_keys="Battle.winner_id", back_populates="winner")
    trades_sent = relationship("Trade", foreign_keys="Trade.sender_id", back_populates="sender")
    trades_received = relationship("Trade", foreign_keys="Trade.receiver_id", back_populates="receiver")
    achievements = relationship("PlayerAchievement", back_populates="player")

    def gain_experience(self, xp):
        self.experience += xp
        while self.experience >= self.required_experience():
            self.level_up()

    def required_experience(self):
        return 100 * self.level

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.money += 50

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'level': self.level,
            'experience': self.experience,
            'money': self.money
        }

# CLI-related logic (can move to player_controller.py)
def create_player(session, username):
    player = Player(username=username)
    session.add(player)
    session.commit()
    return player

def get_player(session, username):
    return session.query(Player).filter_by(username=username).first()

def view_profile(player):
    print(f"\nTrainer Profile: {player.username}")
    print(f"Level: {player.level} | XP: {player.experience}/{player.required_experience()} | Money: ${player.money}")
