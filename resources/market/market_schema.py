""" Market Schema """
"""_summary_
This file to abstract any validation logic for the Market
"""

from dataclasses import dataclass


@dataclass
class MarketPrice:
    name: str
    symbol: str
    price: float
