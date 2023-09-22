"""05.09.2023-23:30:53

Revision ID: 97e7ca33c69c
Revises: 5bb4b99aaf74
Create Date: 2023-09-05 23:31:00.833470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97e7ca33c69c'
down_revision: Union[str, None] = '5bb4b99aaf74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('images', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('stars', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stars', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('images', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
