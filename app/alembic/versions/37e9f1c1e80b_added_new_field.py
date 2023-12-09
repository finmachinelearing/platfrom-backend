"""added new field

Revision ID: 37e9f1c1e80b
Revises: b77ed5505abe
Create Date: 2023-12-09 20:11:06.795091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e9f1c1e80b'
down_revision: Union[str, None] = 'b77ed5505abe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'task',
        sa.Column('test_data', sa.String, nullable=True, default=None)
    )


def downgrade() -> None:
    pass
