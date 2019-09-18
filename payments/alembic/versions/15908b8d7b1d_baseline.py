"""baseline

Revision ID: 15908b8d7b1d
Revises: 
Create Date: 2019-09-18 10:44:13.246988

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15908b8d7b1d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.VARCHAR(length=255), nullable=False),
    sa.Column('amount', mysql.JSON(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=225), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('item_details', mysql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('payment_id', sa.VARCHAR(length=255), nullable=False),
    sa.Column('amount', mysql.JSON(), nullable=False),
    sa.Column('order_id', sa.VARCHAR(length=255), nullable=False),
    sa.Column('payment_details', mysql.JSON(), nullable=False),
    sa.Column('payment_status', sa.VARCHAR(length=225), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('order')
    # ### end Alembic commands ###
