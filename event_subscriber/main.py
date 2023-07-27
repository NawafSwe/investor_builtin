import json
import uuid
import aio_pika
from fastapi.logger import logger

from api.config import Settings
from mixins.Message import Message
from resources.alerts.alert_schema import CreateAlertCommand
from resources.alerts.alert_service import notify_threshold_reached

settings = Settings()


class EventHandler:

    def __init__(self):
        self._mq_url = f"amqp://{settings.BROKER_USERNAME}:{settings.BROKER_USERNAME}@{settings.BROKER_HOST}"
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(url="amqp://guest:guest@rabbitmq-node:5672/")
        self.channel = await self.connection.channel()

    async def subscribe(
            self,
            exchange_key: str = None,
            router_key: str = None,
            exchange_type: str = None,
            queue: str = None,
            durable: bool = False,
    ):
        await self.channel.set_qos(prefetch_count=1)
        exchange = await self.channel.declare_exchange(
            name=exchange_key,
            type=exchange_type,
        )
        queue = await self.channel.declare_queue(name=queue, durable=durable)
        await queue.bind(exchange, routing_key=router_key)
        await queue.consume(self.message_callback)

    async def close_connection(self):
        await self.connection.close()

    @staticmethod
    async def message_callback(message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
            correlation_id = message.headers.get("correlation_id")
            print("self._mq_url: " +  f"amqp://{settings.BROKER_USERNAME}:{settings.BROKER_USERNAME}@{settings.BROKER_HOST}")
            print("[message received]:", correlation_id, " ---- [body]: ", body)
            if body:
                body = json.loads(body)
                await notify_threshold_reached(CreateAlertCommand(**body))

    async def publish(
            self,
            exchange_key: str = None,
            router_key: str = None,
            exchange_type: str = None,
            message: Message = None,
    ):
        exchange = await self.channel.declare_exchange(
            name=exchange_key,
            type=exchange_type,
        )
        props = {"correlation_id": str(uuid.uuid4())}
        await exchange.publish(
            aio_pika.Message(body=json.dumps(message.dict()).encode('utf-8'), headers=props),
            routing_key=router_key,
        )
