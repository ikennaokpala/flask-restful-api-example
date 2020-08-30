"""Create mzxml files table

Revision ID: f03b3c1288a8
Revises: 58dbe451cb20
Create Date: 2020-06-17 08:49:56.380907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f03b3c1288a8'
down_revision = '58dbe451cb20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'mzxml_files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.TEXT(), nullable=True),
        sa.Column('extension', sa.String(), nullable=True),
        sa.Column('location', sa.TEXT(), nullable=True),
        sa.Column('checksum', sa.String(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['projects.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_mzxml_files_checksum'), 'mzxml_files', ['checksum'], unique=False
    )
    op.create_index(
        op.f('ix_mzxml_files_created_at'), 'mzxml_files', ['created_at'], unique=False
    )
    op.create_index(
        op.f('ix_mzxml_files_extension'), 'mzxml_files', ['extension'], unique=False
    )
    op.create_index(
        op.f('ix_mzxml_files_location'), 'mzxml_files', ['location'], unique=False
    )
    op.create_index(op.f('ix_mzxml_files_name'), 'mzxml_files', ['name'], unique=False)
    op.create_index(
        op.f('ix_mzxml_files_updated_at'), 'mzxml_files', ['updated_at'], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mzxml_files_updated_at'), table_name='mzxml_files')
    op.drop_index(op.f('ix_mzxml_files_name'), table_name='mzxml_files')
    op.drop_index(op.f('ix_mzxml_files_location'), table_name='mzxml_files')
    op.drop_index(op.f('ix_mzxml_files_extension'), table_name='mzxml_files')
    op.drop_index(op.f('ix_mzxml_files_created_at'), table_name='mzxml_files')
    op.drop_index(op.f('ix_mzxml_files_checksum'), table_name='mzxml_files')
    op.drop_table('mzxml_files')
    # ### end Alembic commands ###
