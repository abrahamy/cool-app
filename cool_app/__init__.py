__version__ = "0.1.0"

import abc
import collections
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

Message = collections.namedtuple("Message", ["name", "email"])


class RabbitMQ(abc.ABC):
    """Implements default event handlers for RabbitMQ"""

    def __init__(self, queue: typing.AnyStr, exchange: typing.AnyStr = ""):
        self.connection = None
        self.channel = None
        self.queue = queue
        self.exchange = exchange

    def on_connection_open(self, connection: pika.connection.Connection):
        """Handle connection open event"""
        log.info("RabbitMQ connection opened")
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel: pika.channel.Channel):
        """Handle channel open event"""
        log.info("RabbitMQ channel opened")
        self.channel = channel
        self.channel.queue_declare(self.on_queue_declared, queue=self.queue)

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
            self.stop()

    def stop(self):
        """Gracefully shut down RabbitMQ connection"""
        log.info("Gracefully shutting down RabbitMQ connection")

        if self.connection is not None:
            self.connection.close()
            self.connection.ioloop.start()
            self.connection = None

        log.info("RabbitMQ connection shutdown completed")
