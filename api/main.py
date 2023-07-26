import asyncio

from uvicorn import run
from fastapi import FastAPI

from api.routes import init_routes
from db.models.model_base import setup_db
from event_subscriber.main import EventHandler
from api.config import Settings

settings = Settings()
app = init_routes(FastAPI())
event_handler = EventHandler()
if __name__ == "__main__":
    setup_db()
    run("api.main:app")


@app.get("/health-check")
async def health():
    return {"status": "ok"}


async def _startup_event():
    await event_handler.connect()
    await event_handler.subscribe(
        exchange_key="alert_threshold",
        router_key="alert_threshold_price_reached",
        queue=settings.ALERTS_QUEUE,
        exchange_type="topic",
    )

    await event_handler.publish(exchange_key="alert_threshold",
                                router_key="alert_threshold_price_reached", exchange_type="topic", message="hello here event")


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    loop.create_task(_startup_event())
