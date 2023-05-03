"""add content column to posts table

Revision ID: d0b939b51dd9
Revises: 840ebeeb3415
Create Date: 2023-03-18 05:51:19.511425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0b939b51dd9'
down_revision = '840ebeeb3415'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts','content')
    pass
