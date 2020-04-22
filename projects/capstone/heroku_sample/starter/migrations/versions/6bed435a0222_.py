"""empty message

Revision ID: 6bed435a0222
Revises: 
Create Date: 2020-04-22 12:53:41.979133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bed435a0222'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('People', sa.Column('age', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('People', 'age')
    # ### end Alembic commands ###