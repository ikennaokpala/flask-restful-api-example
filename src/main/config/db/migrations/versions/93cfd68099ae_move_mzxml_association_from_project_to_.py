"""Move MZXml association from project to data types

Revision ID: 93cfd68099ae
Revises: 25cbeee570b1
Create Date: 2020-08-07 06:54:06.640677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93cfd68099ae'
down_revision = '25cbeee570b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'mzxml_files', sa.Column('data_type_id', sa.Integer(), nullable=False)
    )
    op.create_index(
        op.f('ix_mzxml_files_data_type_id'),
        'mzxml_files',
        ['data_type_id'],
        unique=False,
    )
    op.drop_constraint('mzxml_files_project_id_fkey', 'mzxml_files', type_='foreignkey')
    op.create_foreign_key(None, 'mzxml_files', 'data_types', ['data_type_id'], ['id'])
    op.drop_column('mzxml_files', 'project_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'mzxml_files',
        sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, 'mzxml_files', type_='foreignkey')
    op.create_foreign_key(
        'mzxml_files_project_id_fkey', 'mzxml_files', 'projects', ['project_id'], ['id']
    )
    op.drop_index(op.f('ix_mzxml_files_data_type_id'), table_name='mzxml_files')
    op.drop_column('mzxml_files', 'data_type_id')
    # ### end Alembic commands ###
