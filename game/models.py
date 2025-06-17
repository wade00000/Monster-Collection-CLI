from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Table
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from game.database import Base 
from datetime import datetime

# --- Association Tables --- (for friend rival system)

friend_association = Table(
    'friend_association', Base.metadata,
    Column('player_id', Integer, ForeignKey('players.id')),
    Column('friend_id', Integer, ForeignKey('players.id'))
)

rival_association = Table(
    'rival_association', Base.metadata,
    Column('player_id', Integer, ForeignKey('players.id')),
    Column('rival_id', Integer, ForeignKey('players.id'))
)


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    money = Column(Integer, default=0)

    friends = relationship(
        "Player",
        secondary=friend_association,
        primaryjoin=id==friend_association.c.player_id,
        secondaryjoin=id==friend_association.c.friend_id,
        backref="friend_of"
    )

    rivals = relationship(
        "Player",
        secondary=rival_association,
        primaryjoin=id==rival_association.c.player_id,
        secondaryjoin=id==rival_association.c.rival_id,
        backref="rival_of"
    )

    monsters = relationship("PlayerMonster", back_populates="owner")
    battles_as_player1 = relationship("Battle", foreign_keys="Battle.player1_id", back_populates="player1")
    battles_as_player2 = relationship("Battle", foreign_keys="Battle.player2_id", back_populates="player2")
    battles_won = relationship("Battle", foreign_keys="Battle.winner_id", back_populates="winner")
    trades_sent = relationship("Trade", foreign_keys="Trade.sender_id", back_populates="sender")
    trades_received = relationship("Trade", foreign_keys="Trade.receiver_id", back_populates="receiver")
    achievements = relationship("PlayerAchievement", back_populates="player")



class MonsterSpecies(Base):
    __tablename__ = 'monster_species'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type_id = Column(Integer, ForeignKey('types.id'))
    base_stats = Column(JSON)
    base_level = Column(Integer, nullable=False, default=1)
    rarity = Column(String)
    abilities = Column(JSON)

    player_monsters = relationship("PlayerMonster", back_populates="species")
    type_obj = relationship("Type", back_populates="monsters")



class PlayerMonster(Base):
    __tablename__ = 'player_monsters'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    species_id = Column(Integer, ForeignKey('monster_species.id'))
    nickname = Column(String)
    level = Column(Integer)
    current_stats = Column(JSON)
    caught_at = Column(DateTime, default=datetime.utcnow)
    xp = Column(Integer, default=0)


    owner = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="player_monsters")
    trade = relationship("Trade", back_populates="monster", uselist=False)



class Battle(Base):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey('players.id'))
    player2_id = Column(Integer, ForeignKey('players.id'))
    winner_id = Column(Integer, ForeignKey('players.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="battles_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="battles_as_player2")
    winner = relationship("Player", foreign_keys=[winner_id], back_populates="battles_won")



class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('players.id'))
    receiver_id = Column(Integer, ForeignKey('players.id'))
    monster_sent = Column(Integer, ForeignKey('player_monsters.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("Player", foreign_keys=[sender_id], back_populates="trades_sent")
    receiver = relationship("Player", foreign_keys=[receiver_id], back_populates="trades_received")
    monster = relationship("PlayerMonster", back_populates="trade")



class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    achievement_name = Column(String, unique=True)
    description = Column(String)
    unlock_condition = Column(String)

    player_achievements = relationship("PlayerAchievement", back_populates="achievement")



class PlayerAchievement(Base):
    __tablename__ = 'player_achievements'

    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="player_achievements")



#Allows us to manage typos & duplicates within types and allow for relationships as opposed to being a column
class Type(Base): 
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    strengths = relationship(
        "TypeEffectiveness",
        foreign_keys="TypeEffectiveness.attacking_type_id",
        back_populates="attacking_type"
    )
    weaknesses = relationship(
        "TypeEffectiveness",
        foreign_keys="TypeEffectiveness.defending_type_id",
        back_populates="defending_type"
    )

    monsters = relationship("MonsterSpecies", back_populates="type_obj")

    

class TypeEffectiveness(Base):
    __tablename__ = 'type_effectiveness'

    id = Column(Integer, primary_key=True)
    attacking_type_id = Column(Integer, ForeignKey('types.id'))
    defending_type_id = Column(Integer, ForeignKey('types.id'))
    multiplier = Column(Integer)  

    attacking_type = relationship("Type", foreign_keys=[attacking_type_id], back_populates="strengths")
    defending_type = relationship("Type", foreign_keys=[defending_type_id], back_populates="weaknesses")




