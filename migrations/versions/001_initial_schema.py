"""initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-05-31
"""

from alembic import op
import sqlalchemy as sa

revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if "password_history" not in tables:
        op.create_table(
            "password_history",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("password", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_password_history_id"), "password_history", ["id"], unique=False)

    if "admin_users" not in tables:
        op.create_table(
            "admin_users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("username", sa.String(), nullable=False),
            sa.Column("password_hash", sa.String(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_admin_users_id"), "admin_users", ["id"], unique=False)
        op.create_index(op.f("ix_admin_users_username"), "admin_users", ["username"], unique=True)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if "admin_users" in tables:
        op.drop_table("admin_users")
    if "password_history" in tables:
        op.drop_table("password_history")
