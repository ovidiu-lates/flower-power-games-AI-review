"""Keep the migration chain compatible with the consolidated base schema.

Revision ID: 3a1039209bd8
Revises: aaf8f5c31fc6
Create Date: 2026-09-18 16:47:55.365800
"""

from typing import Sequence, Union


revision: str = "3a1039209bd8"
down_revision: Union[str, Sequence[str], None] = "aaf8f5c31fc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
