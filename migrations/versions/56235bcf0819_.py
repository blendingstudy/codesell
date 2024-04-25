"""empty message

Revision ID: 56235bcf0819
Revises: bb474ab55d27
Create Date: 2024-04-25 17:25:14.685285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56235bcf0819'
down_revision = 'bb474ab55d27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###
