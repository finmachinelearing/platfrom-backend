"""added default value

Revision ID: 7a086c67a41b
Revises: 5120ca4f41ed
Create Date: 2023-11-11 16:51:41.403120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a086c67a41b'
down_revision: Union[str, None] = '5120ca4f41ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'about', default=None)


def downgrade() -> None:
    pass
