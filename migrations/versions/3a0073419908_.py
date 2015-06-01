"""empty message

Revision ID: 3a0073419908
Revises: c352487997f
Create Date: 2015-06-01 20:53:03.500350

"""

# revision identifiers, used by Alembic.
revision = '3a0073419908'
down_revision = 'c352487997f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.rename_table('submission', 'thing')
    op.alter_column('thing', 'submission_id', new_column_name='reddit_id')
    op.add_column('thing', sa.Column('type', sa.String(length=50), nullable=True))
    op.add_column('thing', sa.Column('body', sa.Text(), nullable=True))
