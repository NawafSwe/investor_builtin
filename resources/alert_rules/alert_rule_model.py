""" Alert Rule Model """
from datetime import datetime

from sqlalchemy import Column, String, Float, UniqueConstraint, Date
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db.models.model_base import Base


class AlertRule(Base):
    __tablename__ = "alerts_rules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    threshold_price = Column(Float(10, 2))
    created_at = Column(Date, nullable=False, default=datetime.now())
    updated_at = Column(Date, nullable=False, default=datetime.now())
    __table_args__ = (
        UniqueConstraint('symbol', 'threshold_price', name='_alert_rule_constraint'),
    )
