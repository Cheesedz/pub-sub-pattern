import pika, json, uuid
from utils import custom_json_serializer

def get_connection():
    """Establish a RabbitMQ connection."""
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))

def get_channel():
    connection = get_connection()
    channel = connection.channel()

    # Declare exchanges
    channel.exchange_declare(exchange='topic_exchange', exchange_type='topic', durable=True)
    channel.exchange_declare(exchange='fanout_exchange', exchange_type='fanout', durable=True)

    # Declare queue and bind it to the topic exchange
    channel.queue_declare(queue='package_queue', durable=True)
    channel.queue_bind(
        exchange='topic_exchange', 
        queue='package_queue', 
        routing_key='package.*'
    )

    channel.queue_declare(queue='delivery_queue', durable=True)
    channel.queue_bind(
        exchange='topic_exchange', 
        queue='delivery_queue', 
        routing_key='delivery.*'
    )

    channel.queue_declare(queue='mail_queue', durable=True)
    channel.queue_bind(
        exchange='fanout_exchange', 
        queue='mail_queue', 
        routing_key='notification.*'
    )

    channel.queue_declare(queue='mail_queue_2', durable=True)
    channel.queue_bind(
        exchange='fanout_exchange', 
        queue='mail_queue_2', 
        routing_key='notification.*'
    )
    

    return connection, channel

def publish(body: dict, exchange: str, routing_key: str | list[str], consumer: str):
    # Get channel and connection
    connection, channel = get_channel()
    
    message_with_celery_body = {
        "args": [json.dumps(body, default=custom_json_serializer)],
        "kwargs": {}
    }

    if isinstance(routing_key, list):
        for key in routing_key:
            channel.basic_publish(
            exchange=exchange,  # Publish to your desired exchange
            routing_key=key,      # Routing key for the queue
            body=json.dumps(message_with_celery_body),
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers={'id': str(uuid.uuid4()), 'task': f'celery_tasks.tasks.{consumer}'},
                content_type='application/json'
            )  # Make message persistent
        )
    
    else:
    # Publish the message
        channel.basic_publish(
            exchange=exchange,  # Publish to your desired exchange
            routing_key=routing_key,      # Routing key for the queue
            body=json.dumps(message_with_celery_body),
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers={'id': str(uuid.uuid4()), 'task': f'celery_tasks.tasks.{consumer}'},
                content_type='application/json'
            )  # Make message persistent
        )

    if connection:
        connection.close()
