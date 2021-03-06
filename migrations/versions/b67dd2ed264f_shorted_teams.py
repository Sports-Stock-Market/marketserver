"""shorted teams

Revision ID: b67dd2ed264f
Revises: c373e9aa16b0
Create Date: 2020-06-06 00:30:00.986478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b67dd2ed264f'
down_revision = 'c373e9aa16b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team', sa.String(length=140), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('num_team', sa.Integer(), nullable=True),
    sa.Column('portfolio_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_short_team_timestamp'), 'short_team', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_short_team_timestamp'), table_name='short_team')
    op.drop_table('short_team')
    # ### end Alembic commands ###
