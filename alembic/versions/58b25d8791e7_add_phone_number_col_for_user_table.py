"""add phone_number col for user table

Revision ID: 58b25d8791e7
Revises:
Create Date: 2025-11-04 18:36:08.090027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58b25d8791e7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column("phone_number",sa.String(15),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
