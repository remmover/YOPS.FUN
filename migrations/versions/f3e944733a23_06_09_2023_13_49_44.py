"""06.09.2023-13:49:44

Revision ID: f3e944733a23
Revises: d2c56e469505
Create Date: 2023-09-06 13:49:51.477453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3e944733a23'
down_revision: Union[str, None] = 'd2c56e469505'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('asset_id', sa.String(length=32), nullable=False))
    op.alter_column('images', 'about',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'about',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('images', 'asset_id')
    # ### end Alembic commands ###