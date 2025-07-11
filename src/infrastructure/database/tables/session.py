from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
    UUID,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from domain.entities.session import Session
from infrastructure.database.tables.base import metadata, mapper_registry
from domain.entities.user import User

sessions_table = Table(
    "sessions",
    metadata,
    Column("id", String(255), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True),
    Column("ip_address", String(45), nullable=True),
    Column("user_agent", Text, nullable=True),
    Column("payload", Text, nullable=False),
    
    # Storing last_activity as an integer (Unix timestamp)
    # Added an index for performance on session cleanup queries.
    Column("last_activity", Integer, nullable=False, index=True),
)


def map_sessions_table() -> None:
    mapper_registry.map_imperatively(
        Session,
        sessions_table,
        properties={"user": relationship(User, back_populates="sessions")},
    )
