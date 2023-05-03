"""create users table

Revision ID: 415bf2f451be
Revises: d0b939b51dd9
Create Date: 2023-03-18 06:03:27.040272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '415bf2f451be'
down_revision = 'd0b939b51dd9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                              sa.PrimaryKeyConstraint('id'),
                              sa.UniqueConstraint('email')
    )
    pass

def downgrade() -> None:
    op.drop_table('users')
    pass