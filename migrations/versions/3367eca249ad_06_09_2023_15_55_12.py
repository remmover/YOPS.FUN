"""06.09.2023-15:55:12

Revision ID: 3367eca249ad
Revises: 6127c384b9cd
Create Date: 2023-09-06 15:55:16.336863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3367eca249ad'
down_revision: Union[str, None] = '6127c384b9cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=63), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('small_image', sa.String(length=255), nullable=False),
    sa.Column('cloud_public_id', sa.String(length=32), nullable=False),
    sa.Column('cloud_version', sa.Integer(), nullable=False),
    sa.Column('about', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cloud_public_id'),
    sa.UniqueConstraint('image'),
    sa.UniqueConstraint('small_image')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('emo_joy', sa.SmallInteger(), nullable=False),
    sa.Column('emo_anger', sa.SmallInteger(), nullable=False),
    sa.Column('emo_sadness', sa.SmallInteger(), nullable=False),
    sa.Column('emo_surprise', sa.SmallInteger(), nullable=False),
    sa.Column('emo_disgust', sa.SmallInteger(), nullable=False),
    sa.Column('emo_fear', sa.SmallInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image_m2m_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.SmallInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stars')
    op.drop_table('image_m2m_tag')
    op.drop_table('comments')
    op.drop_table('images')
    op.drop_table('tags')
    op.drop_table('logouts')
    # ### end Alembic commands ###
