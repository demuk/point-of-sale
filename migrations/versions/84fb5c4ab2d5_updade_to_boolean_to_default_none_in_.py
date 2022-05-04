""" updade to boolean to default none in user model

Revision ID: 84fb5c4ab2d5
Revises: 5b71df9547ee
Create Date: 2022-05-04 11:44:30.665261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84fb5c4ab2d5'
down_revision = '5b71df9547ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), nullable=True))
    op.drop_column('user', 'active')
    # ### end Alembic commands ###
