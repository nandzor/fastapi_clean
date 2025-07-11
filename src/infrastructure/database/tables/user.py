from sqlalchemy import (
    String,
    Table,
    Column,
    Boolean,
    UUID,
    DateTime,
    Text,
    BigInteger,
    ForeignKey,
    func,
)

from domain.entities.user import User
from infrastructure.database.tables.base import metadata, mapper_registry

users_table = Table(
    "users",
    metadata,
    # Core User Fields (from original + Laravel)
    Column("id", UUID, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("email", String(256), unique=True, nullable=False),
    Column("email_verified_at", DateTime, nullable=True),
    Column("hashed_password", String(1024), nullable=False),
    Column("remember_token", String(100), nullable=True),
    
    # Timestamps (managed by the database)
    Column("created_at", DateTime, server_default=func.now(), nullable=True),
    Column("updated_at", DateTime, onupdate=func.now(), nullable=True),

    # Role and Type Fields
    Column("level", String(50), nullable=True),
    Column("type_login", String(50), nullable=True),
    Column("is_active", Boolean, default=True, nullable=False),

    # Foreign Keys to other tables
    Column("clients_id", BigInteger, ForeignKey("clients.id"), nullable=True),
    Column("business_unit_id", BigInteger, ForeignKey("business_units.id"), nullable=True),
    Column("cluster_id", BigInteger, ForeignKey("clusters.id"), nullable=True),

    # Additional Contact/Info Fields
    Column("address", Text, nullable=True),
    Column("handphone", String(25), nullable=True),
    Column("tele_id", String(50), nullable=True),
    Column("tele_channel", String(100), nullable=True),
)


def map_users_table() -> None:
    """Maps the users_table to the User domain entity."""
    mapper_registry.map_imperatively(User, users_table)