from alembic import op
import sqlalchemy as sa


"""

Revision ID: 1b3cad05731a
Revises: 161c3081124e
Create Date: 2022-05-05 08:34:26.500516

"""

# revision identifiers, used by Alembic.
revision = '1b3cad05731a'
down_revision = '161c3081124e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('ix_items_description', table_name='items')
    op.drop_index('ix_items_id', table_name='items')
    op.drop_index('ix_items_title', table_name='items')
    op.drop_table('items')


def downgrade() -> None:
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='items_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_index('ix_items_title', 'items', ['title'], unique=False)
    op.create_index('ix_items_id', 'items', ['id'], unique=False)
    op.create_index('ix_items_description', 'items', ['description'], unique=False)
