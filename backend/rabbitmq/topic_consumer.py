from client import get_connection

channel = get_connection()

channel.queue_declare(queue='package_queue', durable=True)

# Bind the queue to the topic exchange with a routing key
channel.queue_bind(
    exchange='topic_exchange',
    queue='package_queue',
    routing_key='package.*'  # Match routing keys for tasks related to packages
)