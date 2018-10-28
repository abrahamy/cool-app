import json
import logging
from multiprocessing import Process

import pika
import sqlalchemy

from cool_app import Message, RabbitMQ
from cool_app.models import Customer, Session

log = logging.getLogger(__name__)


class RabbitMQConsumer(RabbitMQ):
    """A consumer for processing rabbitmq messages"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_queue_declared(self, frame: pika.frame.Frame):
        """Handle queue declared event"""
        log.info("RabbitMQ queue declared")
        self.queue = frame.method.queue
        self.channel.basic_consume(
            self.process_message, queue=self.queue, no_ack=True, exclusive=True
        )

    def process_message(self, channel, method, properties, body):
        """Process received messages"""
        log.info("Saving message to database")
        data = json.loads(body)
        message = Message(*data)
        self.store(message)

    @classmethod
    def store(cls, message: Message):
        """Stores the message into a database"""
        session = Session()

        try:
            customer = Customer(name=message.name, email=message.email)
            session.add(customer)
            session.commit()
            log.info("Message persisted successfully")
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
        finally:
            session.close()


def start_consumer(*args):
    """Start the rabbitmq consumer"""
    consumer = RabbitMQConsumer("coolapp")
    consumer.start()
