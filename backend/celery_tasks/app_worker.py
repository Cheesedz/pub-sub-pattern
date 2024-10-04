import os
from celery import Celery

BROKER_URI = 'pyamqp://'
BACKEND_URI = 'rpc://'

app = Celery(
    'celery_tasks',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_tasks.tasks']
)

app.conf.task_routes = {
    'tasks.package_consumer': {
        'queue': 'package_queue',
        'routing_key': 'package.*'
    }
}
