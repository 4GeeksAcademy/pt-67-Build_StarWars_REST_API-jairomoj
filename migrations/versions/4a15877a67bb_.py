"""empty message

Revision ID: 4a15877a67bb
Revises: fcba30e8c931
Create Date: 2024-07-06 17:59:25.790397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a15877a67bb'
down_revision = 'fcba30e8c931'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('climate', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('model', sa.String(length=40), nullable=False),
    sa.Column('_class', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fav_character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('char_relation', sa.Integer(), nullable=False),
    sa.Column('user_relation', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['char_relation'], ['character.id'], ),
    sa.ForeignKeyConstraint(['user_relation'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fav_planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_relation', sa.Integer(), nullable=False),
    sa.Column('user_relation', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_relation'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_relation'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fav_vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehic_relation', sa.Integer(), nullable=False),
    sa.Column('user_relation', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_relation'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vehic_relation'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fav_vehicle')
    op.drop_table('fav_planet')
    op.drop_table('fav_character')
    op.drop_table('vehicle')
    op.drop_table('planet')
    # ### end Alembic commands ###
