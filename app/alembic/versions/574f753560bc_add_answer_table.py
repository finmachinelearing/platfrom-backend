"""add answer table

Revision ID: 574f753560bc
Revises: 47582c77855b
Create Date: 2023-11-12 17:18:41.845879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '574f753560bc'
down_revision: Union[str, None] = '47582c77855b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'answer',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('task_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
        sa.Column('task_ans', sa.JSON),
        sa.Column('score', sa.Float, nullable=True, default=None),
        sa.Column('added_at', sa.DateTime),
        sa.Column('is_active', sa.Boolean)
    )
    op.create_foreign_key(
        'answer_to_task',
        'answer',
        'task',
        ['task_id'],
        ['id']
    )
    op.create_foreign_key(
        'answer_to_user',
        'answer',
        'user',
        ['user_id'],
        ['id']
    )


def downgrade() -> None:
    pass
