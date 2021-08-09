"""empty message

Revision ID: c98eb56ef373
Revises: 429297c9fd36
Create Date: 2021-08-07 00:01:21.895626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c98eb56ef373'
down_revision = '429297c9fd36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('song',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('duration', sa.String(length=100), nullable=True),
    sa.Column('genre', sa.String(), nullable=False),
    sa.Column('bpm', sa.String(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('user_token', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_token'], ['user.token'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_table('song')
    # ### end Alembic commands ###