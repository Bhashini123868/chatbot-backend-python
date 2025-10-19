"""creating tablie

Revision ID: fcd3be7dcb3d
Revises: a39b40353b3c
Create Date: 2025-10-14 15:24:18.224656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcd3be7dcb3d'
down_revision: Union[str, Sequence[str], None] = 'a39b40353b3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
