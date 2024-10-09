from fastapi import APIRouter, HTTPException
from backend.models.model import Payment
from rabbitmq.client import get_connection, get_channel, publish
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
    try:
        publish(
            body=body.model_dump(),
            exchange='topic_exchange',
            routing_key='package.created',
            consumer='package_consumer'
        )

        return {"status": "Message Published"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/listen")
async def process_webhook(data: dict):
    logging.info(f"WebHook: {data}")
    try:
        match data['topic']:
            case 'delivery':
                publish(
                    body=data,
                    exchange='topic_exchange',
                    routing_key='delivery.created',
                    consumer='delivery_consumer'
                )
            case 'notification':
                publish(
                    body=data,
                    exchange='fanout_exchange',
                    routing_key='notification.mail',
                    consumer='mail_noti_consumer'
                )

        return {"status": "Message Published"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
