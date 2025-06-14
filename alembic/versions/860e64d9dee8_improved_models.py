"""improved models

Revision ID: 860e64d9dee8
Revises: 8c104748ec7e
Create Date: 2025-06-13 15:24:19.908796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '860e64d9dee8'
down_revision: Union[str, None] = '8c104748ec7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('achievement_name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('unlock_condition', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('achievement_name')
    )
    op.create_table('monster_species',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('base_stats', sqlite.JSON(), nullable=True),
    sa.Column('rarity', sa.String(), nullable=True),
    sa.Column('abilities', sqlite.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('battles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player1_id', sa.Integer(), nullable=True),
    sa.Column('player2_id', sa.Integer(), nullable=True),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['player1_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['player2_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player_achievements',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('achievement_name', sa.String(), nullable=False),
    sa.Column('unlocked_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['achievement_name'], ['achievements.achievement_name'], ),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('player_id', 'achievement_name')
    )
    op.create_table('player_monsters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('species_id', sa.Integer(), nullable=True),
    sa.Column('nickname', sa.String(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('current_stats', sqlite.JSON(), nullable=True),
    sa.Column('caught_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['species_id'], ['monster_species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('monster_sent', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['monster_sent'], ['player_monsters.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('monsters')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monsters',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('level', sa.INTEGER(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('trades')
    op.drop_table('player_monsters')
    op.drop_table('player_achievements')
    op.drop_table('battles')
    op.drop_table('monster_species')
    op.drop_table('achievements')
    # ### end Alembic commands ###
