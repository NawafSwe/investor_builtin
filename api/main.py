import asyncio

from uvicorn import run
from fastapi import FastAPI

from api.routes import init_routes
from db.models.model_base import setup_db
from event_subscriber.main import EventHandler
from api.config import Settings
from resources.alerts.alert_schema import CreateAlertCommand

settings = Settings()
app = init_routes(FastAPI())
event_handler = EventHandler()
if __name__ == "__main__":
    setup_db()
    run("api.main:app")


@app.get("/health-check")
async def health():
    await event_handler.publish(exchange_key="alert_threshold",
                                router_key="alert_threshold_price_reached",
                                exchange_type="topic",
                                message=CreateAlertCommand(
                                    symbol="HealthCheck",
                                    original_threshold_price="0",
                                    new_price="0",
                                    name="Checking broker health",
                                ))

    return {"status": "ok"}


async def _startup_event():
    await event_handler.connect()
    await event_handler.subscribe(
        exchange_key="alert_threshold",
        router_key="alert_threshold_price_reached",
        queue=settings.ALERTS_QUEUE,
        exchange_type="topic",
    )


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    loop.create_task(_startup_event())
