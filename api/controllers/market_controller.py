from fastapi import APIRouter
from resources.market.market_service import get_market_data

router = APIRouter()


@router.get("/")
def get_market_data_route(decimal_places: int = 2):
    prices = get_market_data(price_decimal_places=decimal_places)
    if prices:
        return {"data": prices, "status": True, "status_code": 200}
    else:
        return {"error": "Something went wrong", "status": False, "status_code": 500}
