"""teams table

Revision ID: 036b44e65133
Revises: cf3b4cb192eb
Create Date: 2020-05-25 11:17:17.864039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036b44e65133'
down_revision = 'cf3b4cb192eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team', sa.String(length=140), nullable=True),
    sa.Column('num_team', sa.Integer(), nullable=True),
    sa.Column('portfolio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    # ### end Alembic commands ###