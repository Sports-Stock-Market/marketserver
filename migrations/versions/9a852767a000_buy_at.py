"""buy at:

Revision ID: 9a852767a000
Revises: b67dd2ed264f
Create Date: 2020-06-08 21:55:08.382439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a852767a000'
down_revision = 'b67dd2ed264f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('short_team', sa.Column('buy_at', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('short_team', 'buy_at')
    # ### end Alembic commands ###
