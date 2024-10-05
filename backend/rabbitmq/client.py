import pika

def get_connection():
    """Establish a RabbitMQ connection."""
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))

def get_channel():
    connection = get_connection()
    channel = connection.channel()

    # Declare exchanges
    channel.exchange_declare(exchange='topic_exchange', exchange_type='topic', durable=True)

    # Declare queue and bind it to the topic exchange
    channel.queue_declare(queue='package_queue', durable=True)
    channel.queue_bind(
        exchange='topic_exchange', 
        queue='package_queue', 
        routing_key='package.*'
    )

    return connection, channel
