from io import BytesIO
from typing import Callable

import pika
from pika.exchange_type import ExchangeType


class RabbitMQServer:

    def __init__(self, connection_url='ampq://localhost'):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_url))
        self._channel = self._connection.channel()

    def consume_topic(self, exchange: str, route: str, cb: Callable[[str, str, ], None]):
        self._channel.exchange_declare(exchange, ExchangeType.topic)
        result = self._channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        self._channel.queue_bind(queue_name, exchange, route)

    def publish_in_topic(self, exchange: str, route: str, message: str):
        self._channel.exchange_declare(exchange, ExchangeType.topic)
        self._channel.basic_publish(exchange, route, bytes(message))

    def __del__(self):
        self._connection.close()
