"""Tag more none nullable fields

Revision ID: 9f5a69dad176
Revises: 6f67cd532eb9
Create Date: 2020-06-18 18:42:25.597286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5a69dad176'
down_revision = '6f67cd532eb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mzxml_files', 'checksum',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('mzxml_files', 'extension',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('mzxml_files', 'location',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('mzxml_files', 'name',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('mzxml_files', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mzxml_files', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('mzxml_files', 'name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('mzxml_files', 'location',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('mzxml_files', 'extension',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('mzxml_files', 'checksum',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
