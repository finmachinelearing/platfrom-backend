"""add name field to task

Revision ID: 47582c77855b
Revises: a9877e676726
Create Date: 2023-11-12 16:37:59.061456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47582c77855b'
down_revision: Union[str, None] = 'a9877e676726'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'task',
        sa.Column('name', sa.String)
    )


def downgrade() -> None:
    pass
