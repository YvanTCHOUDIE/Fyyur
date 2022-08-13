"""empty message

Revision ID: a8ff295911e6
Revises: 8e35e02c624d
Create Date: 2022-08-13 19:29:08.985802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8ff295911e6'
down_revision = '8e35e02c624d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genres')
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'website')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'website')
    op.drop_table('show')
    # ### end Alembic commands ###
