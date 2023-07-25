""" Alert Rule Schema """
"""_summary_
This file to abstract any validation logic for the Alert Rules
"""
from pydantic import BaseModel
from decimal import Decimal


class AlertRuleCreate(BaseModel):
    name: str
    symbol: str
    threshold_price: Decimal
