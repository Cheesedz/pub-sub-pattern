from fastapi import APIRouter, HTTPException
from backend.models.model import Payment
from rabbitmq.client import get_connection
from celery_tasks.tasks import package_consumer
import json
import pika
from utils import custom_json_serializer

router = APIRouter()

@router.get('/')
async def index():
    return {'message': 'Hello World'}

@router.post('/payment')
async def paid(body: Payment):
    try:
        channel = get_connection()
        channel.basic_publish(
            exchange='',
            routing_key='generic',
            body=json.dumps(body.model_dump(), default=custom_json_serializer),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        return {"status": "Message Published"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")