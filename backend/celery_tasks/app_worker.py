from celery import Celery

BROKER_URI = 'pyamqp://'
BACKEND_URI = 'rpc://'

app = Celery(
    'celery_tasks',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_tasks.tasks']
)

# Task Routing with Custom Queues and Routing Keys
app.conf.task_routes = {
    'celery_tasks.tasks.package_consumer': {
        'queue': 'package_queue',
        'routing_key': 'package.*'  # This matches your RabbitMQ routing
    }
}