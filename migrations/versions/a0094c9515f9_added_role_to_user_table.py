"""added role to User table

Revision ID: a0094c9515f9
Revises: 495e42f2b6ea
Create Date: 2018-12-20 10:40:25.713643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0094c9515f9'
down_revision = '495e42f2b6ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.drop_column('user', 'role')
    # ### end Alembic commands ###
