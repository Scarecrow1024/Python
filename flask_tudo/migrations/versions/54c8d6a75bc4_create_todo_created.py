"""'create_todo_created'

Revision ID: 54c8d6a75bc4
Revises: 60dd59d6527f
Create Date: 2017-08-12 22:18:39.408659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54c8d6a75bc4'
down_revision = '60dd59d6527f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todo', 'created')
    # ### end Alembic commands ###