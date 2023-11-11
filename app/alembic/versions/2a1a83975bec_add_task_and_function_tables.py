"""add task and function tables

Revision ID: 2a1a83975bec
Revises: a9a4107f1f70
Create Date: 2023-11-11 19:33:28.409100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a1a83975bec'
down_revision: Union[str, None] = 'a9a4107f1f70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('short_description', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('start_date', sa.DateTime),
        sa.Column('end_date', sa.DateTime),
        sa.Column('function_id', sa.Integer),
        sa.Column('task_data', sa.String),
        sa.Column('task_ans', sa.JSON),
        sa.Column('ans_type', sa.String),
        sa.Column('is_active', sa.Boolean)
    )
    op.create_table(
        'function',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String)
    )
    op.create_foreign_key(
        'task_to_function',
        'task',
        'function',
        ['function_id'],
        ['id']
    )


def downgrade() -> None:
    pass
