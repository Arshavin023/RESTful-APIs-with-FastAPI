"""create users table

Revision ID: 74bc32d7cd1a
Revises: d0b939b51dd9
Create Date: 2023-03-18 06:12:19.959973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74bc32d7cd1a'
down_revision = '415bf2f451be'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('posts',sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",
                          local_cols=["user_id"],remote_cols=["id"],ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','user_id')
    pass

