"""make game text columns unicode

Revision ID: d7e5f2c8a901
Revises: c4f1b6e2a7d9
Create Date: 2026-09-21 15:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d7e5f2c8a901"
down_revision: str | Sequence[str] | None = "c4f1b6e2a7d9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        DECLARE @constraint_name sysname;
        DECLARE @sql nvarchar(max);
        SELECT @constraint_name = kc.name
        FROM sys.key_constraints AS kc
        INNER JOIN sys.index_columns AS ic
            ON kc.parent_object_id = ic.object_id
            AND kc.unique_index_id = ic.index_id
        INNER JOIN sys.columns AS c
            ON ic.object_id = c.object_id
            AND ic.column_id = c.column_id
        WHERE kc.parent_object_id = OBJECT_ID(N'dbo.game')
            AND kc.type = 'UQ'
            AND c.name = N'name'
            AND ic.key_ordinal = 1;

        IF @constraint_name IS NOT NULL
        BEGIN
            SET @sql = N'ALTER TABLE dbo.game DROP CONSTRAINT '
                + QUOTENAME(@constraint_name);
            EXEC sys.sp_executesql @sql;
        END;
        """
    )
    op.alter_column(
        "game",
        "name",
        existing_type=sa.String(length=255),
        type_=sa.Unicode(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        "game",
        "description",
        existing_type=sa.Text(),
        type_=sa.UnicodeText(),
        existing_nullable=False,
    )
    op.alter_column(
        "game",
        "image_url",
        existing_type=sa.String(length=2048),
        type_=sa.Unicode(length=2048),
        existing_nullable=False,
    )
    op.create_unique_constraint("uq_game_name", "game", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_game_name", "game", type_="unique")
    op.alter_column(
        "game",
        "image_url",
        existing_type=sa.Unicode(length=2048),
        type_=sa.String(length=2048),
        existing_nullable=False,
    )
    op.alter_column(
        "game",
        "description",
        existing_type=sa.UnicodeText(),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.alter_column(
        "game",
        "name",
        existing_type=sa.Unicode(length=255),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.create_unique_constraint("uq_game_name", "game", ["name"])