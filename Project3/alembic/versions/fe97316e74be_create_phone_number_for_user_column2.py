"""Create phone number for user column2

Revision ID: fe97316e74be
Revises: f47f40e2293c
Create Date: 2025-05-28 13:22:56.448005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe97316e74be'
down_revision: Union[str, None] = 'f47f40e2293c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')

