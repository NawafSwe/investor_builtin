from fastapi import APIRouter
from resources.market.market_service import get_market_data

router = APIRouter()


@router.get("/")
def get_market_data_route(decimal_places: int = 2):
    return get_market_data(price_decimal_places=decimal_places)
