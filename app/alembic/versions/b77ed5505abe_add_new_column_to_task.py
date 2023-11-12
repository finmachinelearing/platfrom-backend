"""add new column to task

Revision ID: b77ed5505abe
Revises: 574f753560bc
Create Date: 2023-11-12 20:03:50.863144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b77ed5505abe'
down_revision: Union[str, None] = '574f753560bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'task',
        sa.Column(
            'tags',
            sa.ARRAY(sa.String)
        )
    )


def downgrade() -> None:
    pass
