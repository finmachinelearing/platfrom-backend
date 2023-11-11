"""add nullable fields

Revision ID: 5120ca4f41ed
Revises: 96b5ef78ee7c
Create Date: 2023-11-11 16:43:10.065102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5120ca4f41ed'
down_revision: Union[str, None] = '96b5ef78ee7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'about', nullable=True)


def downgrade() -> None:
    pass
