"""creating tabloie

Revision ID: 28bfcfa85804
Revises: fcd3be7dcb3d
Create Date: 2025-10-14 15:26:51.421541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28bfcfa85804'
down_revision: Union[str, Sequence[str], None] = 'fcd3be7dcb3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
