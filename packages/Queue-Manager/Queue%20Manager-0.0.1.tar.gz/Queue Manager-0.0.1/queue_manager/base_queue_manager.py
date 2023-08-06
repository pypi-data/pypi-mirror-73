import pika


class BaseQueueManager:

    def __init__(self, amqp_url, exchange_name):
        self.credentials = pika.URLParameters(amqp_url)
        self.exchange_name = exchange_name

    def __enter__(self):
        self.connection = pika.BlockingConnection(self.credentials)
        self.channel = self.connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
