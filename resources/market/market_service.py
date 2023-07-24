""" Market Service """
"""_summary_
this file to write any business logic for the Market
"""

from requests import get
from constants.symbols import Symbol
from api.config import Settings

settings = Settings()


def _construct_symbols_str():
    symbols = ""
    for s in Symbol:
        symbols += s.value + ","
    return symbols


def get_market_data():
    api_key = settings.TWELVE_DATA_API_KEY

    params = {"symbol": _construct_symbols_str(), "dp": 2}
    response = get("https://api.twelvedata.com/price",
                   params=params,
                   headers={"Content-Type": "application/json", "Authorization": f"apikey {api_key}"})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.content, "status": response.status_code}
