"""This migration is fixing problem with missed fields from model

Revision ID: f9997aa23571
Revises: 49952fde9c90
Create Date: 2020-06-19 15:05:58.304672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9997aa23571'
down_revision = '49952fde9c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('activation_date', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('subscriptions', sa.Column('expiry_date', sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Sqlite doesn't support standard drop_column func,
    # so we need to use context manager with batch_alter_table
    # and make deletion, creation process for whole table
    with op.batch_alter_table('subscriptions') as sub_batch_op:
        sub_batch_op.drop_column('expiry_date')
        sub_batch_op.drop_column('activation_date')
    # ### end Alembic commands ###
