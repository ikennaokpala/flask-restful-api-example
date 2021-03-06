"""Add slug to project table

Revision ID: ccca068a9718
Revises: d5f1cca5f2a4
Create Date: 2020-06-09 02:26:58.847794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccca068a9718'
down_revision = 'd5f1cca5f2a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('slug', sa.TEXT(), nullable=True))
    op.create_index(op.f('ix_projects_slug'), 'projects', ['slug'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_projects_slug'), table_name='projects')
    op.drop_column('projects', 'slug')
    # ### end Alembic commands ###
