"""create user table

Revision ID: 96b5ef78ee7c
Revises: 
Create Date: 2023-11-07 21:48:39.913240

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import EmailType


# revision identifiers, used by Alembic.
revision: str = '96b5ef78ee7c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('provider_id', sa.String, index=True),
        sa.Column('name', sa.String),
        sa.Column('surname', sa.String),
        sa.Column('about', sa.Text),
        sa.Column('avatar_url', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('email', EmailType),
        sa.Column('is_superuser', sa.Boolean, default=False),
        sa.Column('joined_date', sa.DateTime, default=datetime.now)
    )


def downgrade() -> None:
    pass
