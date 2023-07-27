from celery import Celery


# Create a celery app object to start your workers

def create_celery_app():
    app = Celery(
        'worker',
        broker='amqp://guest:guest@rabbitmq-node:5672/',
        include=['resources.market.tasks']
    )
    app.conf.update(
        broker_connection_retry=True,
        broker_connection_retry_on_startup=True
    )
    return app
