from alembic import op
import sqlalchemy as sa


"""

Revision ID: 161c3081124e
Revises: 681fd1e6d3e3
Create Date: 2022-04-28 11:54:38.370566

"""

# revision identifiers, used by Alembic.
revision = '161c3081124e'
down_revision = '681fd1e6d3e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('comments', 'object_id', new_column_name='commentable_object_id')
    op.alter_column('comments', 'object_type', new_column_name='commentable_object_type')


def downgrade() -> None:
    op.alter_column('comments', 'commentable_object_id', new_column_name='object_id')
    op.alter_column('comments', 'commentable_object_type', new_column_name='object_type')
