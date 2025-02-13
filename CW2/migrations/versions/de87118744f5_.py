"""empty message

Revision ID: de87118744f5
Revises: 26d570d1ec68
Create Date: 2024-12-02 23:09:16.852381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de87118744f5'
down_revision = '26d570d1ec68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes_count', sa.Integer(), nullable=True))
        batch_op.drop_column('likes')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.INTEGER(), nullable=True))
        batch_op.drop_column('likes_count')

    # ### end Alembic commands ###
