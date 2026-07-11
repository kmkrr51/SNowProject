from sqlalchemy import Column, String, DateTime, Text, Index
from datetime import datetime
from ...shared.infrastructure import Base


class SearchIndexModel(Base):
  __tablename__ = "search_indexes"

  id = Column(String(50), primary_key=True)
  entity_id = Column(String(50), nullable=False)
  entity_type = Column(String(50), nullable=False)
  title = Column(String(255), nullable=False)
  description = Column(String(2000), nullable=False)
  content = Column(Text, nullable=False)
  search_metadata = Column(Text, nullable=True)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  __table_args__ = (
    Index("idx_search_entity_type", "entity_type"),
    Index("idx_search_updated_at", "updated_at"),
  )
