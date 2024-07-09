"""add comment table

Revision ID: 7741d70d0931
Revises: b27ae8cd0b70
Create Date: 2024-07-06 14:06:02.588808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7741d70d0931'
down_revision = 'b27ae8cd0b70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=1023), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###