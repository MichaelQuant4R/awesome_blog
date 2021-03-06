"""m-2

Revision ID: 47233e0b2b5f
Revises: 1e76d57a6660
Create Date: 2020-11-23 23:44:15.320389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47233e0b2b5f'
down_revision = '1e76d57a6660'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
