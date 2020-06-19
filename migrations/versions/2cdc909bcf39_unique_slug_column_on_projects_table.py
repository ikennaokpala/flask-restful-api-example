"""Unique slug column on projects table

Revision ID: 2cdc909bcf39
Revises: f03b3c1288a8
Create Date: 2020-06-18 18:38:05.111352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cdc909bcf39'
down_revision = 'f03b3c1288a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_projects_slug', table_name='projects')
    op.create_index(op.f('ix_projects_slug'), 'projects', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_projects_slug'), table_name='projects')
    op.create_index('ix_projects_slug', 'projects', ['slug'], unique=False)
    # ### end Alembic commands ###
