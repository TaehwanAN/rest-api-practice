"""empty message

Revision ID: ca3e98622bdf
Revises: dd6c1b80e6f9
Create Date: 2025-02-09 02:03:47.618239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3e98622bdf'
down_revision = 'dd6c1b80e6f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customers')
    # ### end Alembic commands ###
