"""add role table

Revision ID: a0c0f59cb9fd
Revises: 7741d70d0931
Create Date: 2024-07-08 21:17:58.506773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0c0f59cb9fd'
down_revision = '7741d70d0931'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=31), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user', 'role')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('role')
    # ### end Alembic commands ###
