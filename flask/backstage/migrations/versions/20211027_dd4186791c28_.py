"""empty message

Revision ID: dd4186791c28
Revises: 1694eeb91f79
Create Date: 2021-10-27 19:55:18.036825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd4186791c28'
down_revision = '1694eeb91f79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('work_role', sa.Column('contract_description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('work_role', 'contract_description')
    # ### end Alembic commands ###
