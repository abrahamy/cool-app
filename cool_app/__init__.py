__version__ = "0.1.0"

import abc
import logging
import sys
import typing

import pika

import cool_app.settings as settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler(settings.LOG_FILE),
    ],
)
log = logging.getLogger(__name__)


class RabbitMQ(abc.ABC):
    """Implements default event handlers for RabbitMQ"""

    def __init__(self, queue: typing.AnyStr):
        self.connection = None
        self.channel = None
        self.queue = queue

    def on_connection_open(self, connection: pika.connection.Connection):
        """Handle connection open event"""
        log.info("RabbitMQ connection opened")
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel: pika.channel.Channel):
        """Handle channel open event"""
        log.info("RabbitMQ channel opened")
        self.channel = channel
        self.channel.queue_declare(
            queue=self.queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self.on_queue_declared,
        )

    @abc.abstractmethod
    def on_queue_declared(self, frame: pika.frame.Frame):
        """Handle queue declared event"""
        pass

    def start(self, rabbit_uri: typing.AnyStr = None):
        """Initialize rabbitmq connection"""
        parameters = pika.URLParameters(rabbit_uri or settings.RABBITMQ_URI)
        connection = pika.SelectConnection(parameters, self.on_connection_open)

        try:
            log.info("Starting IO loop")
            connection.ioloop.start()
        except KeyboardInterrupt:
            log.info("Gracefully shutting down RabbitMQ connection")
            connection.close()
            connection.ioloop.start()
            log.info("RabbitMQ connection shutdown completed")
