"""create PDF-aligned review schema

Revision ID: aaf8f5c31fc6
Revises:
Create Date: 2026-09-16 15:55:31.761715
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "aaf8f5c31fc6"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def uuid_column() -> sa.Uuid:
    return sa.Uuid(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "game",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("min_players", sa.Integer(), nullable=True),
        sa.Column("max_players", sa.Integer(), nullable=True),
        sa.Column("min_play_time", sa.Integer(), nullable=True),
        sa.Column("max_play_time", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "review",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("user_id", uuid_column(), nullable=False),
        sa.Column("game_id", uuid_column(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "game_insight",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("game_id", uuid_column(), nullable=False),
        sa.Column("total_reviews", sa.Integer(), nullable=False),
        sa.Column("average_rating", sa.Float(), nullable=False),
        sa.Column("positive_percentage", sa.Float(), nullable=False),
        sa.Column("neutral_percentage", sa.Float(), nullable=False),
        sa.Column("negative_percentage", sa.Float(), nullable=False),
        sa.Column("easy_percentage", sa.Float(), nullable=False),
        sa.Column("medium_percentage", sa.Float(), nullable=False),
        sa.Column("hard_percentage", sa.Float(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "review_analysis",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("review_id", uuid_column(), nullable=False),
        sa.Column("sentiment", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("perceived_difficulty", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["review_id"], ["review.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("review_id"),
    )
    op.create_table(
        "review_liked_aspect",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("review_analysis_id", uuid_column(), nullable=False),
        sa.Column("aspect", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["review_analysis_id"], ["review_analysis.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "review_complaint",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("review_analysis_id", uuid_column(), nullable=False),
        sa.Column("complaint", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["review_analysis_id"], ["review_analysis.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "game_insight_liked_aspect",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("game_insight_id", uuid_column(), nullable=False),
        sa.Column("aspect", sa.String(length=255), nullable=False),
        sa.Column("occurrence_count", sa.Integer(), nullable=False),
        sa.Column("percentage", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["game_insight_id"], ["game_insight.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "game_insight_complaint",
        sa.Column("id", uuid_column(), nullable=False),
        sa.Column("game_insight_id", uuid_column(), nullable=False),
        sa.Column("complaint", sa.String(length=255), nullable=False),
        sa.Column("occurrence_count", sa.Integer(), nullable=False),
        sa.Column("percentage", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["game_insight_id"], ["game_insight.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("game_insight_complaint")
    op.drop_table("game_insight_liked_aspect")
    op.drop_table("review_complaint")
    op.drop_table("review_liked_aspect")
    op.drop_table("review_analysis")
    op.drop_table("game_insight")
    op.drop_table("review")
    op.drop_table("game")
    op.drop_table("user")
