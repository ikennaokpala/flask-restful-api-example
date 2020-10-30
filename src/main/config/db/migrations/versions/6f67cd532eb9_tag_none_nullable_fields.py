"""Tag none nullable fields

Revision ID: 6f67cd532eb9
Revises: 2cdc909bcf39
Create Date: 2020-06-18 18:40:29.426827

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6f67cd532eb9'
down_revision = '2cdc909bcf39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'name', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('projects', 'owner', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('projects', 'slug', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('sessions', 'access_token', existing_type=sa.TEXT(), nullable=False)
    op.alter_column(
        'sessions',
        'tokenized_user',
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'sessions',
        'tokenized_user',
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
    )
    op.alter_column('sessions', 'access_token', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('projects', 'slug', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('projects', 'owner', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('projects', 'name', existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###