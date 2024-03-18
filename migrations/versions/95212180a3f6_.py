"""empty message

Revision ID: 95212180a3f6
Revises: 30b24ba2518e
Create Date: 2024-03-19 01:22:10.945251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95212180a3f6'
down_revision = '30b24ba2518e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###