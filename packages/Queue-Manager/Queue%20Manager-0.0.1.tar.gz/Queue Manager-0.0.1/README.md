# Riftool Queue Manager

### QueueConsumer Example
```python
from queue_manager import QueueConsumer
with QueueConsumer(amqp_url='http://queue/url', exchange_name='logs') as consumer:
    consumer.start_consuming()
```

### QueueProducer Example
```python
from queue_manager import QueueProducer
with QueueProducer(amqp_url='http://queue/url', exchange_name='logs', queue_arguments={}) as producer:
    producer.publish(priority=10, message='Message')
```