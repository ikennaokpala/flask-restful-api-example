"""Define pipelines table

Revision ID: 126a76db90da
Revises: 4e127ae580da
Create Date: 2020-12-15 02:50:13.028683

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '126a76db90da'
down_revision = '4e127ae580da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'pipelines',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.TEXT(), nullable=True),
        sa.Column('data_type_id', sa.Integer(), nullable=False),
        sa.Column('prototype_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['prototype_id'], ['prototypes.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['data_type_id'], ['data_types.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )
    op.create_index(
        op.f('ix_pipelines_prototype_id'), 'pipelines', ['prototype_id'], unique=False
    )
    op.create_index(
        op.f('ix_pipelines_created_at'), 'pipelines', ['created_at'], unique=False
    )
    op.create_index(
        op.f('ix_pipelines_data_type_id'), 'pipelines', ['data_type_id'], unique=False
    )
    op.create_index(op.f('ix_pipelines_name'), 'pipelines', ['name'], unique=False)
    op.create_index(
        op.f('ix_pipelines_updated_at'), 'pipelines', ['updated_at'], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pipelines_updated_at'), table_name='pipelines')
    op.drop_index(op.f('ix_pipelines_name'), table_name='pipelines')
    op.drop_index(op.f('ix_pipelines_data_type_id'), table_name='pipelines')
    op.drop_index(op.f('ix_pipelines_created_at'), table_name='pipelines')
    op.drop_index(op.f('ix_pipelines_prototype_id'), table_name='pipelines')
    op.drop_table('pipelines')
    # ### end Alembic commands ###
