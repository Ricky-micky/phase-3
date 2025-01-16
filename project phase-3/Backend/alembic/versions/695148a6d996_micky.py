"""micky

Revision ID: 695148a6d996
Revises: 959414bf0078
Create Date: 2024-12-18 00:01:33.582204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '695148a6d996'
down_revision: Union[str, None] = '959414bf0078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
