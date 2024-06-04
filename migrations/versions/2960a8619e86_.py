"""empty message

Revision ID: 2960a8619e86
Revises: 7361a971eda1
Create Date: 2024-05-26 09:13:21.499050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2960a8619e86'
down_revision = '7361a971eda1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('demo_link', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'demo_link')
    # ### end Alembic commands ###