from rabbitmq.client import get_connection
import json
from utils import custom_json_serializer

# Reuse the channel from the rabbitmq_client
channel = get_connection()

# Consumer callback
def generic_consumer(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")

    # Republish to the topic exchange with a dynamic routing key
    routing_key = 'package.created'  # Modify routing key as needed
    channel.basic_publish(
        exchange='topic_exchange',
        routing_key=routing_key,
        body=json.dumps(message, default=custom_json_serializer)
    )
    print(f"Message forwarded to topic_exchange with routing key {routing_key}")

# Set up the consumer to listen to the 'generic' queue
channel.basic_consume(
    queue='generic',
    on_message_callback=generic_consumer,
    auto_ack=True
)

# Start consuming messages
print("Waiting for messages in generic queue...")
channel.start_consuming()
