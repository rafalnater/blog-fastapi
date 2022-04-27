from alembic import op
import sqlalchemy as sa


"""

Revision ID: 681fd1e6d3e3
Revises: c74dfef0e43b
Create Date: 2022-04-27 14:28:20.746963

"""

# revision identifiers, used by Alembic.
revision = '681fd1e6d3e3'
down_revision = 'c74dfef0e43b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('object_type', sa.Unicode(length=255), nullable=True),
    sa.Column('object_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
