"""Polymorphic Single Table Inheritance on data_format_files for mzxml and metadata shipment tables

Revision ID: aa5e4ee929db
Revises: c4d7c3b4a79f
Create Date: 2020-08-13 06:50:38.123045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aa5e4ee929db'
down_revision = 'c4d7c3b4a79f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'data_format_files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.TEXT(), nullable=False),
        sa.Column('extension', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('data_type_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('location', sa.TEXT(), nullable=True),
        sa.Column('checksum', sa.String(), nullable=True),
        sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['data_type_id'], ['data_types.id'],),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_data_format_files_created_at'),
        'data_format_files',
        ['created_at'],
        unique=False,
    )
    op.create_index(
        op.f('ix_data_format_files_data_type_id'),
        'data_format_files',
        ['data_type_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_data_format_files_extension'),
        'data_format_files',
        ['extension'],
        unique=False,
    )
    op.create_index(
        op.f('ix_data_format_files_name'), 'data_format_files', ['name'], unique=False
    )
    op.create_index(
        op.f('ix_data_format_files_updated_at'),
        'data_format_files',
        ['updated_at'],
        unique=False,
    )
    op.drop_table('mzxml_files')
    op.drop_table('metadata_shipments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'metadata_shipments',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('file_name', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('extension', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            'content',
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            'updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column('data_type_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['data_type_id'],
            ['data_types.id'],
            name='metadata_shipments_data_type_id_fkey',
        ),
        sa.PrimaryKeyConstraint('id', name='metadata_shipments_pkey'),
    )
    op.create_table(
        'mzxml_files',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('extension', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('location', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('checksum', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            'created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            'updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column('data_type_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['data_type_id'], ['data_types.id'], name='mzxml_files_data_type_id_fkey'
        ),
        sa.PrimaryKeyConstraint('id', name='mzxml_files_pkey'),
    )
    op.drop_index(
        op.f('ix_data_format_files_updated_at'), table_name='data_format_files'
    )
    op.drop_index(op.f('ix_data_format_files_name'), table_name='data_format_files')
    op.drop_index(
        op.f('ix_data_format_files_extension'), table_name='data_format_files'
    )
    op.drop_index(
        op.f('ix_data_format_files_data_type_id'), table_name='data_format_files'
    )
    op.drop_index(
        op.f('ix_data_format_files_created_at'), table_name='data_format_files'
    )
    op.drop_table('data_format_files')
    # ### end Alembic commands ###