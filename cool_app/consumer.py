import logging

import pika

from cool_app import RabbitMQ


log = logging.getLogger(__name__)


class RabbitMQConsumer(RabbitMQ):
    """A consumer for processing rabbitmq messages"""

    def on_queue_declared(self, frame: pika.frame.Frame):
        """Handle queue declared event"""
        log.info("RabbitMQ queue declared")
        self.channel.basic_consume(self.process_message, queue=self.queue)

    def process_message(self, method, head, body):
        """Process received messages"""
        pass
