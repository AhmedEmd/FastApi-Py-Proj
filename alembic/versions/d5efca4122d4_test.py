"""test

Revision ID: d5efca4122d4
Revises: 
Create Date: 2024-02-07 13:25:17.912454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5efca4122d4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Testing',  # Table name
        sa.Column('column_name', sa.Integer)  # Add column example
    )


def downgrade() -> None:
    pass
