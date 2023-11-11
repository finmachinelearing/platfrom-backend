"""update task data in task table

Revision ID: a9877e676726
Revises: 2a1a83975bec
Create Date: 2023-11-11 20:03:01.147415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9877e676726'
down_revision: Union[str, None] = '2a1a83975bec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('task', 'task_data', nullable=True)


def downgrade() -> None:
    pass
