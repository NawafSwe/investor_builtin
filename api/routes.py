from api.controllers.market_controller import router as market_router
from api.controllers.rules_controller import router as rules_router


def init_routes(app):
    app.include_router(market_router, prefix="/market-prices", tags=["Market"])
    app.include_router(rules_router, prefix="/alert-rules", tags=["Alert-Rules"])
    return app
