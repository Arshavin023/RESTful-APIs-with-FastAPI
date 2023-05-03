"""add last few columns to posts table

Revision ID: 6552239906c1
Revises: 74bc32d7cd1a
Create Date: 2023-03-18 06:37:02.850706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6552239906c1'
down_revision = '74bc32d7cd1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column(
        "published",sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column("posts",sa.Column(
        "created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')
    ))

def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    
