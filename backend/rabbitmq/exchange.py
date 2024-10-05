from client import get_channel

connection, channel = get_channel()

channel.exchange_declare(exchange='topic_exchange', exchange_type='topic')
channel.exchange_declare(exchange='fanout_exchange', exchange_type='fanout')
channel.exchange_bind(destination='fanout_exchange', source='topic_exchange', routing_key='topic_fanout')