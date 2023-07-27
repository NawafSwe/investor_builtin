import asyncio
import threading

from celery.schedules import crontab
from fastapi.logger import logger
from sqlalchemy.orm import Session
from uvicorn import run
from fastapi import FastAPI, Depends

from api.routes import init_routes
from db.models.model_base import setup_db, get_db
from event_subscriber.main import EventHandler
from api.config import Settings
from resources.alerts.alert_dal import AlertRepository
from resources.alerts.alert_schema import CreateAlertCommand
from worker.app import create_celery_app

settings = Settings()
app = init_routes(FastAPI())
celery_app = create_celery_app()
logger.info("settings.BROKER_HOST: " + settings.BROKER_HOST)
logger.info("settings.BROKER_HOST: " + settings.DB_HOST)
celery_app.conf.beat_schedule = {
    'fetch_market_data_every_minute': {
        'task': 'resources.market.tasks.fetch_market_data_every_minute',
        'schedule': crontab(minute='*'),
    },
}
celery_app.autodiscover_tasks()
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

@app.get("/view-alerts")
def view_alerts(db: Session = Depends(get_db)):
    return AlertRepository(db).find_all()


async def _startup_event():
    await event_handler.connect()
    await event_handler.subscribe(
        exchange_key="alert_threshold",
        router_key="alert_threshold_price_reached",
        queue=settings.ALERTS_QUEUE,
        exchange_type="topic",
    )


def start_celery_worker():
    t = threading.Thread(target=celery_app.worker_main, kwargs={'argv': ['worker', '--loglevel=INFO']})
    t.start()
    from resources.market import tasks



@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    loop.create_task(_startup_event())


app.add_event_handler('startup', start_celery_worker)
