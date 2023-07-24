from api.controllers.market_controller import router as market_router


def init_routes(app):
    app.include_router(market_router, prefix="/market-prices", tags=["Market"])
    return app
