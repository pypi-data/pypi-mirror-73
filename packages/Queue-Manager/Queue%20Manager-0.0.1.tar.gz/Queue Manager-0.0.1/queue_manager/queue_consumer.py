from queue_manager.base_queue_manager import BaseQueueManager


class QueueConsumer(BaseQueueManager):

    def __enter__(self):
        super(QueueConsumer, self).__enter__()
        self._bind_to_exchange()
        return self

    def _bind_to_exchange(self) -> None:
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.channel.queue_bind(exchange=self.exchange_name, queue=result.method.queue)
        self._tmp_queue_name = result.method.queue

    def start_consuming(self, message_callback):
        self.channel.basic_consume(queue=self._tmp_queue_name, on_message_callback=message_callback, exclusive=True)
        self.channel.start_consuming()
