import asyncio
import json
import uuid
from functools import partial
from typing import Callable

import aio_pika
from aiormq.abc import DeliveredMessage
from pika import BasicProperties

from api.config import Settings

# Create a connection object to start consuming events
settings = Settings()


class EventHandler:

    def __init__(self):
        self._mq_url = f"amqp://{settings.BROKER_USERNAME}:{settings.BROKER_USERNAME}@{settings.BROKER_HOST}"
        self._exchange_key = "alert_threshold"
        self._router_key = "alert_threshold_price_reached"
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(url=self._mq_url)
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
            print("message received here, id: ", correlation_id)
            print("message received here, body: ", body)
            # await callback(body, correlation_id)

    async def publish(
            self,
            exchange_key: str = None,
            router_key: str = None,
            exchange_type: str = None,
            message: str = None,
    ):
        exchange = await self.channel.declare_exchange(
            name=exchange_key,
            type=exchange_type,
        )
        props = {"correlation_id": str(uuid.uuid4())}
        await exchange.publish(
            aio_pika.Message(body=message.encode(), headers=props),
            routing_key=router_key,
        )
