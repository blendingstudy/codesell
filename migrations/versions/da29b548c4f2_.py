"""empty message

Revision ID: da29b548c4f2
Revises: 56235bcf0819
Create Date: 2024-04-26 01:15:24.812371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da29b548c4f2'
down_revision = '56235bcf0819'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('participations_user_id_fkey', 'participations', type_='foreignkey')
    op.create_foreign_key(None, 'participations', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'participations', type_='foreignkey')
    op.create_foreign_key('participations_user_id_fkey', 'participations', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###