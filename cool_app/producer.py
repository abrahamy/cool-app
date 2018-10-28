import json
import logging
import time
import typing

import pika

from cool_app import Message, RabbitMQ

log = logging.getLogger(__name__)


class RabbitMQProducer(RabbitMQ):
    """A producer for publishing rabbitmq messages"""

    def __init__(self, outbox: typing.List[Message], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outbox = outbox
        self.failed_deliveries = []

    def on_queue_declared(self, frame: pika.frame.Frame):
        """Handle queue declared event"""
        log.info("RabbitMQ queue declared")
        log.info("Sending all messages in outbox")

        message_count = len(self.outbox)

        for message in self.outbox:
            self.publish_message(message)
            time.sleep(1)

        fail_count = len(self.failed_deliveries)
        log.info(f"{fail_count}/{message_count} delivered successfully")

        self.stop()

    def publish_message(self, message: Message):
        """Publish a message to rabbitmq"""
        properties = pika.BasicProperties(
            content_type="application/json", content_encoding="utf8"
        )

        try:
            self.channel.basic_publish(
                self.exchange,
                self.queue,
                json.dumps(message, ensure_ascii=False),
                properties,
            )
            log.info("Message published to rabbitmq")
        except Exception:
            log.exception(f"Delivery failed for {message}")
            self.failed_deliveries.append(message)
