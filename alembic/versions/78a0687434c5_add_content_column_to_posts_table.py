"""add content column to posts table

Revision ID: 78a0687434c5
Revises: 2b0d9e547988
Create Date: 2023-09-01 12:55:47.408780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78a0687434c5'
down_revision: Union[str, None] = '2b0d9e547988'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
