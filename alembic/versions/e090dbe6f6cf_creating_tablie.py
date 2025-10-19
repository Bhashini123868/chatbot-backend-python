"""creating tablie

Revision ID: e090dbe6f6cf
Revises: 28bfcfa85804
Create Date: 2025-10-14 15:28:23.525098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e090dbe6f6cf'
down_revision: Union[str, Sequence[str], None] = '28bfcfa85804'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
