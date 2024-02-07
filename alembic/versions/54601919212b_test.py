"""test

Revision ID: 54601919212b
Revises: d5efca4122d4
Create Date: 2024-02-07 13:40:46.056781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54601919212b'
down_revision: Union[str, None] = 'd5efca4122d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
