""" This migration is adding Versions table

Revision ID: bf9c7c171b23
Revises: f9997aa23571
Create Date: 2020-06-19 15:56:14.940517

"""
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf9c7c171b23'
down_revision = 'f9997aa23571'
branch_labels = None
depends_on = None


def populate_versions(versions):
    op.bulk_insert(versions, [
        {
            'id': 1,
            'effective_date_start': datetime(2019, 8, 1, tzinfo=timezone.utc),
            'effective_date_end': datetime(2019, 9, 1, tzinfo=timezone.utc),
            "creation_date": datetime(2019, 8, 1, tzinfo=timezone.utc),
            "subscription_id": 1,
            "plan_id": 3
        },
        {
            'id': 2,
            'effective_date_start': datetime(2019, 9, 1, tzinfo=timezone.utc),
            'effective_date_end': datetime(2019, 10, 1, tzinfo=timezone.utc),
            "creation_date": datetime(2019, 8, 1, tzinfo=timezone.utc),
            "subscription_id": 2,
            "plan_id": 1
        },
        {
            'id': 3,
            'effective_date_start': datetime(2019, 10, 1, tzinfo=timezone.utc),
            'effective_date_end': datetime(2019, 11, 1, tzinfo=timezone.utc),
            "creation_date": datetime(2019, 10, 1, tzinfo=timezone.utc),
            "subscription_id": 2,
            "plan_id": 2
        }
    ])


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    versions = op.create_table(
        'versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('effective_date_start', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('effective_date_end', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('creation_date', sa.TIMESTAMP(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], )
    )
    populate_versions(versions)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('versions')
    # ### end Alembic commands ###
