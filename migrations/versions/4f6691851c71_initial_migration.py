"""Initial migration.

Revision ID: 4f6691851c71
Revises: 
Create Date: 2021-04-22 11:32:28.139515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f6691851c71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctor', sa.Column('specialization', sa.String(length=100), nullable=True))
    op.add_column('patient', sa.Column('disease_description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patient', 'disease_description')
    op.drop_column('doctor', 'specialization')
    # ### end Alembic commands ###