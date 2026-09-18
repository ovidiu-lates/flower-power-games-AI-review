"""add user auth fields and username uniqueness

Revision ID: c4f1b6e2a7d9
Revises: 3a1039209bd8
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c4f1b6e2a7d9"
down_revision: str | Sequence[str] | None = "3a1039209bd8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_unique_constraint("uq_user_username", "user", ["username"])
    op.create_index("ix_user_username", "user", ["username"], unique=False)
    op.alter_column("user", "is_active", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_user_username", table_name="user")
    op.drop_constraint("uq_user_username", "user", type_="unique")
    op.drop_column("user", "is_active")
