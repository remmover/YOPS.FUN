"""11.09.2023-18:08:49

Revision ID: 2db535160138
Revises: c67f10694867
Create Date: 2023-09-11 18:08:57.955158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2db535160138'
down_revision: Union[str, None] = 'c67f10694867'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag_m2m_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image_id', 'tag_id', name='tag_image')
    )
    op.drop_table('image_m2m_tag')
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('images', sa.Column('small_image', sa.String(length=255), nullable=False))
    op.add_column('images', sa.Column('cloud_public_id', sa.String(length=32), nullable=False))
    op.add_column('images', sa.Column('cloud_version', sa.Integer(), nullable=False))
    op.add_column('images', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('images', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.alter_column('images', 'about',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('images', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_unique_constraint(None, 'images', ['small_image'])
    op.create_unique_constraint(None, 'images', ['cloud_public_id'])
    op.alter_column('stars', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stars', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'images', type_='unique')
    op.drop_constraint(None, 'images', type_='unique')
    op.alter_column('images', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('images', 'about',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_column('images', 'updated_at')
    op.drop_column('images', 'created_at')
    op.drop_column('images', 'cloud_version')
    op.drop_column('images', 'cloud_public_id')
    op.drop_column('images', 'small_image')
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_table('image_m2m_tag',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='image_m2m_tag_image_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='image_m2m_tag_tag_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='image_m2m_tag_pkey')
    )
    op.drop_table('tag_m2m_image')
    # ### end Alembic commands ###
