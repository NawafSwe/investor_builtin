""" Alert Model """
import uuid
from datetime import datetime

from sqlalchemy import Column, String, UUID, Date

from db.models.model_base import Base


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    original_threshold_price = Column(String, nullable=False)
    reached_threshold_price = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())
    updated_at = Column(Date, nullable=False, default=datetime.now())
