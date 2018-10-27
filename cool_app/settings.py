import os


LOG_FILE = os.getenv("LOG_FILE", "cool-app.log")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://")
