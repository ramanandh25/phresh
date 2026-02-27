"""create_main_tables

Revision ID: 571ca0679147
Revises:
Create Date: 2026-02-23 16:23:17.429426

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "571ca0679147"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_cleanings_table() -> None:
    """Create cleanings table."""
    op.create_table(
        "cleanings",
        sa.Column("ID", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "cleaning_type", sa.Text, nullable=False, server_default="spot_cleaning"
        ),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )


def upgrade() -> None:
    """Upgrade schema."""
    create_cleanings_table()


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("cleanings")
