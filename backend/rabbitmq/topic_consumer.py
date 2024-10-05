from rabbitmq.client import get_connection, get_channel
import json
from celery_tasks.tasks import package_consumer

# Reuse the channel from the rabbitmq_client
connection, channel = get_channel()

def topic_consumer(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"Received message from RabbitMQ: {message}")

        # Send the message to Celery task worker
        package_consumer.apply_async(args=[message])

        print(f"Message forwarded to Celery task worker")

        # Acknowledge the message after successfully forwarding to Celery
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Set up the consumer to listen to the 'package_queue'
channel.basic_consume(queue='package_queue', on_message_callback=topic_consumer, auto_ack=False)

# Start consuming messages
print("Waiting for messages in package_queue...")
channel.start_consuming()
