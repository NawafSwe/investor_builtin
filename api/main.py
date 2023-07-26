import asyncio

from uvicorn import run
from fastapi import FastAPI

from api.routes import init_routes
from db.models.model_base import setup_db
from event_subscriber.main import setup_pika_connection

app = init_routes(FastAPI())

if __name__ == "__main__":
    setup_db()
    run("api.main:app")


@app.get("/health_check")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup_event():
    loop = asyncio.get_running_loop()
    loop.create_task(setup_pika_connection())
