"""add token blacklist table

Revision ID: a9a4107f1f70
Revises: 7a086c67a41b
Create Date: 2023-11-11 17:14:14.464455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a4107f1f70'
down_revision: Union[str, None] = '7a086c67a41b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'token_blacklist',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('token', sa.String)
    )


def downgrade() -> None:
    pass
