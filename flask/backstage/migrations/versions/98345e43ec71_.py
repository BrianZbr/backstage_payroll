"""empty message

Revision ID: 98345e43ec71
Revises: 8ec98a77f252
Create Date: 2021-10-29 18:34:58.570321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98345e43ec71'
down_revision = '8ec98a77f252'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('time_worked_employee_id_key', 'time_worked', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('time_worked_employee_id_key', 'time_worked', ['employee_id'])
    # ### end Alembic commands ###