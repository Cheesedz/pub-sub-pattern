from fastapi import APIRouter, HTTPException
from backend.models.model import Payment
from rabbitmq.client import get_connection, get_channel
from celery_tasks.tasks import package_consumer, app
from celery.result import AsyncResult
import json, uuid, pika, logging
from utils import custom_json_serializer

router = APIRouter()

@router.get('/')
async def index():
    return {'message': 'Hello World'}

@router.post('/payment')
async def paid(body: Payment):
    """Handles incoming payments and publishes the event to RabbitMQ."""
    connection, channel = None, None
    try:
        # Get channel and connection
        connection, channel = get_channel()
        
        message_with_celery_body = {
            "args": [json.dumps(body.model_dump(), default=custom_json_serializer)],
            "kwargs": {}
        }

        # Publish the message
        channel.basic_publish(
            exchange='topic_exchange',  # Publish to your desired exchange
            routing_key='package.created',      # Routing key for the queue
            body=json.dumps(message_with_celery_body),
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers={'id': str(uuid.uuid4()), 'task': 'celery_tasks.tasks.package_consumer'},
                content_type='application/json'
            )  # Make message persistent
        )

        return {"status": "Message Published"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        # Ensure the connection is closed after publishing
        if connection:
            connection.close()

@router.post("/listen")
async def get_task_status(data: dict):
    logging.info(f"WebHook: {data}")
    return data
