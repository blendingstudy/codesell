"""empty message

Revision ID: c2832050a16f
Revises: 49f781251ff5
Create Date: 2024-05-08 04:04:47.896537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2832050a16f'
down_revision = '49f781251ff5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fundings', 'creator_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('fundings_creator_id_fkey', 'fundings', type_='foreignkey')
    op.create_foreign_key(None, 'fundings', 'users', ['creator_id'], ['id'], ondelete='SET NULL')
    op.alter_column('products', 'code_file',
               existing_type=sa.VARCHAR(length=200),
               nullable=False,
               existing_server_default=sa.text("''::character varying"))
    op.alter_column('products', 'seller_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('1'))
    op.drop_constraint('products_seller_id_fkey', 'products', type_='foreignkey')
    op.create_foreign_key(None, 'products', 'users', ['seller_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.create_foreign_key('products_seller_id_fkey', 'products', 'users', ['seller_id'], ['id'])
    op.alter_column('products', 'seller_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('1'))
    op.alter_column('products', 'code_file',
               existing_type=sa.VARCHAR(length=200),
               nullable=True,
               existing_server_default=sa.text("''::character varying"))
    op.drop_constraint(None, 'fundings', type_='foreignkey')
    op.create_foreign_key('fundings_creator_id_fkey', 'fundings', 'users', ['creator_id'], ['id'])
    op.alter_column('fundings', 'creator_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
