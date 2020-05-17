"""empty message

Revision ID: e2dc40fc7cc7
Revises: 778eb626a992
Create Date: 2020-05-14 23:59:45.734340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2dc40fc7cc7'
down_revision = '778eb626a992'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weibo', sa.Column('updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weibo', 'updated')
    # ### end Alembic commands ###