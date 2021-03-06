"""empty message

Revision ID: 25d42b668125
Revises: bbb621f56189
Create Date: 2020-05-16 00:55:38.359262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25d42b668125'
down_revision = 'bbb621f56189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'wid')
    )
    op.add_column('weibo', sa.Column('n_like', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weibo', 'n_like')
    op.drop_table('like')
    # ### end Alembic commands ###
