import json
import logging
from multiprocessing import Process

import pika
import sqlalchemy

from cool_app import Message, RabbitMQ
from cool_app.models import Customer, Session

log = logging.getLogger(__name__)


def persist_message(message: Message):
    """Stores the message into a database"""
    session = Session()

    try:
        customer = Customer(name=message.name, email=message.email)
        session.add(customer)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
    except Exception:
        log.exception("Unexpected error")
    finally:
        session.close()


class RabbitMQConsumer(RabbitMQ):
    """A consumer for processing rabbitmq messages"""

    def on_queue_declared(self, frame: pika.frame.Frame):
        """Handle queue declared event"""
        log.info("RabbitMQ queue declared")
        self.channel.basic_consume(self.process_message, queue=self.queue)

    def process_message(self, method, head, body):
        """Process received messages"""
        data = json.loads(body)
        message = Message(*data)
        p = Process(target=persist_message, args=(message,))
        p.start()
