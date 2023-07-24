""" Alert Rule Model """
from sqlalchemy import Column, Integer, String, Float

from db.models.model_base import Base


class AlertRule(Base):
    __tablename__ = "alerts_rules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    symbol = Column(String, unique=True, index=True, nullable=False)
    threshold_price = Column(Float(10, 2))
