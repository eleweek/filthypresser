"""empty message

Revision ID: 582255b4e5d
Revises: 1329cc1d89df
Create Date: 2015-06-01 22:38:10.255059

"""

# revision identifiers, used by Alembic.
revision = '582255b4e5d'
down_revision = '1329cc1d89df'

from alembic import op


def upgrade():
    op.drop_column('thing', 'id')
    op.create_primary_key('pk_thing', 'thing', ['reddit_id'])
