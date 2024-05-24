"""empty message

Revision ID: 47dc880b7336
Revises: fc5ffd0f28f4
Create Date: 2024-05-24 17:03:08.120378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47dc880b7336'
down_revision = 'fc5ffd0f28f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photographer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=1000), nullable=False))
        batch_op.add_column(sa.Column('profile_pic', sa.String(length=250), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.create_unique_constraint('uq_photographer_profile_pic', ['profile_pic'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photographer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.drop_column('profile_pic')
        batch_op.drop_column('about_me')

    # ### end Alembic commands ###
