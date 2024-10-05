from rabbitmq.client import get_connection, get_channel
import json, logging
from celery_tasks.tasks import package_consumer, app

# Reuse the channel from the rabbitmq_client
connection, channel = get_channel()

def topic_consumer(ch, method, properties, body):
    try:
        message = json.loads(body)

        # Send the message to Celery task worker
        task = package_consumer.apply_async(args=[message])
        task_id = task.id

        # Check the task status later
        # Log task submission
        logging.info(f"Task {task_id} has been submitted for processing.")

        # Acknowledge the message after successfully forwarding to Celery
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Set up the consumer to listen to the 'package_queue'
channel.basic_consume(queue='package_queue', on_message_callback=topic_consumer, auto_ack=True)

# Start consuming messages
print("Waiting for messages in package_queue...")
channel.start_consuming()
