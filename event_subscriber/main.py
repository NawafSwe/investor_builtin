import json

import aiormq
from fastapi.logger import logger


from api.config import Settings

# Create a connection object to start consuming events
settings = Settings()


async def setup_pika_connection():
    # create connection
    mq_url = f"amqp://{settings.BROKER_USERNAME}:{settings.BROKER_USERNAME}@{settings.BROKER_HOST}"
    connection = await aiormq.connect(url=mq_url)
    # create channel
    channel = await connection.channel()
    # create queue
    await channel.queue_declare(queue=settings.ALERTS_QUEUE)

    async def callback(channel, body, envelope, properties):
        from resources.alerts.alert_service import create_alert
        correlation_id = properties.correlation_id
        logger.log(f"Received message with correlation ID {correlation_id}: {body}")
        await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
        if body:
            create_alert(json.loads(body))

    # Start consuming messages from the queue
    await channel.basic_consume(queue=settings.ALERTS_QUEUE, consumer_callback=callback)
