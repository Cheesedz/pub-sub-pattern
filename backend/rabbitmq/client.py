import pika
from utils import custom_json_serializer
import json

def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='topic_exchange', 
        exchange_type='topic'
    )
    channel.exchange_declare(
        exchange='fanout_exchange', 
        exchange_type='fanout'
    )
    channel.exchange_bind(
        destination='fanout_exchange', 
        source='topic_exchange', 
        routing_key='topic_fanout'
    )
    channel.queue_declare(
        queue='generic', 
        exclusive=False, 
        durable=True
    )
    return channel