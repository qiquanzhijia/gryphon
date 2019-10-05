"""2nd update datum_indicator table

Revision ID: 88247700113
Revises: 2c23c2ee654d
Create Date: 2019-07-30 00:06:21.360502

"""

# revision identifiers, used by Alembic.
revision = '88247700113'
down_revision = '2c23c2ee654d'


from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import DATETIME

from gryphon.lib.models.exchange import JSONEncodedMoneyDict
sa.JSONEncodedMoneyDict = JSONEncodedMoneyDict


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datum_indicators',
    sa.Column('unique_id', sa.Unicode(length=64), nullable=False),
    sa.Column('datum_id', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.DateTime(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('datum_type', sa.Unicode(length=256), nullable=False),
    sa.Column('exchange', sa.Unicode(length=64), nullable=True),
    sa.Column('numeric_value', sa.Numeric(precision=20, scale=4), nullable=True),
    sa.Column('string_value', sa.Unicode(length=256), nullable=True),
    sa.Column('meta_data', sa.UnicodeText(length=2147483648), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('datum_id'),
    )

    # Indices.
    op.create_index('timestamp', 'datum_indicators', ['timestamp'])

    # Unique Constraints
    op.create_unique_constraint(
        name='di_uid',
        source='datum_indicators', 
        local_cols=['datum_type', 'timestamp', 'exchange', 'numeric_value']
        )
    ### end Alembic commands ###



def downgrade():
    op.drop_table('datum_indicators')