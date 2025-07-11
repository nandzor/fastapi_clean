"""initial migration

Revision ID: 1e22094deddc
Revises: 
Create Date: 2025-07-11 17:47:54.421495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e22094deddc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'users' table
    op.create_table(
        "users",
        # Core User Fields
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(256), unique=True, nullable=False),
        sa.Column("email_verified_at", sa.DateTime, nullable=True),
        sa.Column("hashed_password", sa.String(1024), nullable=False),
        sa.Column("remember_token", sa.String(100), nullable=True),
        
        # Timestamps
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime, onupdate=sa.func.now(), nullable=True),

        # Role and Type Fields
        sa.Column("level", sa.String(50), nullable=True),
        sa.Column("type_login", sa.String(50), nullable=True),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),

        # NOTE: Foreign keys are commented out because the referenced tables
        # ('clients', 'business_units', 'clusters') are not created in this migration.
        # You must create those tables first, then create a new migration
        # to add these columns and their foreign key constraints.
        # sa.Column("clients_id", sa.BigInteger, sa.ForeignKey("clients.id"), nullable=True),
        # sa.Column("business_unit_id", sa.BigInteger, sa.ForeignKey("business_units.id"), nullable=True),
        # sa.Column("cluster_id", sa.BigInteger, sa.ForeignKey("clusters.id"), nullable=True),

        # Additional Contact/Info Fields
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("handphone", sa.String(25), nullable=True),
        sa.Column("tele_id", sa.String(50), nullable=True),
        sa.Column("tele_channel", sa.String(100), nullable=True),
    )

    # Create the 'sessions' table
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id"), nullable=True, index=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("payload", sa.Text, nullable=False),
        sa.Column("last_activity", sa.Integer, nullable=False, index=True),
    )


def downgrade() -> None:
    op.drop_table("sessions")
    op.drop_table("users")
