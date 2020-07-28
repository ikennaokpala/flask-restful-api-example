"""Add metadata_shipments table

Revision ID: 88f42f5fc666
Revises: 9f5a69dad176
Create Date: 2020-07-27 10:04:19.389862

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '88f42f5fc666'
down_revision = '9f5a69dad176'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metadata_shipments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.TEXT(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('raw_file_id', sa.Integer(), nullable=False),
    sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['raw_file_id'], ['raw_files.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_metadata_shipments_created_at'), 'metadata_shipments', ['created_at'], unique=False)
    op.create_index(op.f('ix_metadata_shipments_file_name'), 'metadata_shipments', ['file_name'], unique=False)
    op.create_index(op.f('ix_metadata_shipments_raw_file_id'), 'metadata_shipments', ['raw_file_id'], unique=False)
    op.create_index(op.f('ix_metadata_shipments_updated_at'), 'metadata_shipments', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_metadata_shipments_updated_at'), table_name='metadata_shipments')
    op.drop_index(op.f('ix_metadata_shipments_raw_file_id'), table_name='metadata_shipments')
    op.drop_index(op.f('ix_metadata_shipments_file_name'), table_name='metadata_shipments')
    op.drop_index(op.f('ix_metadata_shipments_created_at'), table_name='metadata_shipments')
    op.drop_table('metadata_shipments')
    # ### end Alembic commands ###
