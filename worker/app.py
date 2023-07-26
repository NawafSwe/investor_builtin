from celery import Celery
# Create a celery app object to start your workers
from api.config import Settings

settings = Settings()


def create_celery_app():
    return Celery('tasks', broker='amqp://localhost')
