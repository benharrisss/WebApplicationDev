"""empty message

Revision ID: 563202bcdbed
Revises: 031fe2fc1ab4
Create Date: 2024-11-27 16:19:46.710163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '563202bcdbed'
down_revision = '031fe2fc1ab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
