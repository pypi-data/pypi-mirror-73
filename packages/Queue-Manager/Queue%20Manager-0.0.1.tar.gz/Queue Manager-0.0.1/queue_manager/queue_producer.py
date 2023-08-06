from pika import BasicProperties
from queue_manager.base_queue_manager import BaseQueueManager


class QueueProducer(BaseQueueManager):

    def __init__(self, queue_arguments, *args, **kwargs):
        super(QueueProducer, self).__init__(*args, **kwargs)
        self.queue_arguments = queue_arguments

    def publish(self, priority, message):
        self.channel.queue_declare(queue='', arguments=self.queue_arguments, exclusive=True)
        properties = BasicProperties(priority=priority)
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='', body=message, properties=properties)
