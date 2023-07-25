""" Alert Rule Schema """
from __future__ import annotations

from typing import Union

from mixins.Message import Command

"""_summary_
This file to abstract any validation logic for the Alert Rules
"""
from pydantic import BaseModel
from decimal import Decimal


class CreateAlertRuleCommand(BaseModel, Command):
    name: str
    symbol: str
    threshold_price: Decimal


class UpdateAlertRuleCommand(BaseModel, Command):
    name: Union[str, None] = None
    symbol: Union[str, None] = None
    threshold_price: Union[Decimal, None] = None
