"""add user employment status

Revision ID: 65a0f1de6260
Revises: 07f0fa35a765
Create Date: 2023-03-18 07:45:18.385436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65a0f1de6260'
down_revision = '07f0fa35a765'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_employment_status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_employment_status')
    # ### end Alembic commands ###