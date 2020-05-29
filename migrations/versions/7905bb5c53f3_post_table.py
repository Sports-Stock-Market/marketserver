"""post table

Revision ID: 7905bb5c53f3
Revises: 1869899c7176
Create Date: 2020-05-25 23:05:38.618567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7905bb5c53f3'
down_revision = '1869899c7176'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team', sa.String(length=140), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('num_team', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
