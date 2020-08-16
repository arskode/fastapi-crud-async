from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func

from src.extensions import metadata


notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(64), nullable=False),
    Column("description", String(64), nullable=False),
    Column("created_at", DateTime, default=func.now(), nullable=False),
)
