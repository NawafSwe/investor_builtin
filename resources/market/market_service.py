""" Market Service """
from resources.market.market_schema import MarketPrice
from requests import get
from constants.stock_symbols import symbol_representation
from api.config import Settings

"""_summary_
this file to write any business logic for the Market
"""

settings = Settings()


def _construct_symbols_str():
    symbols = ""
    for s in symbol_representation.keys():
        symbols += s + ","
    return symbols


def get_market_data(price_decimal_places: int):
    api_key = settings.TWELVE_DATA_API_KEY
    market_prices: list[MarketPrice] = []
    params = {"symbol": _construct_symbols_str(), "dp": price_decimal_places}
    response = get("https://api.twelvedata.com/price",
                   params=params,
                   headers={"Content-Type": "application/json", "Authorization": f"apikey {api_key}"})
    if response.status_code == 200:
        for symbol, value in response.json().items():
            market_prices.append(
                MarketPrice(
                    name=symbol_representation[symbol]['name'],
                    symbol=symbol,
                    price=value["price"]
                    , ))

        return market_prices
