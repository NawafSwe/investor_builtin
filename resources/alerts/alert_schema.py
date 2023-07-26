""" Alert Schema """

from mixins.Message import Command
from pydantic import BaseModel

"""_summary_
This file to abstract any validation logic for the Alerts
"""


class CreateAlertCommand(BaseModel, Command):
    symbol: str
    name: str
    original_threshold_price: str
    reached_threshold_price: str
