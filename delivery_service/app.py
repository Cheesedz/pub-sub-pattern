from dotenv import load_dotenv
import os, requests, json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Package, Delivery
import logging, uuid, random
from utils import custom_json_serializer
from datetime import datetime, timedelta

origins = ["*"]

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    return "Hello"

@app.post('/api/delivery')
async def createDelivery(data: Package):
    try:
        delivery = Delivery(
            delivery_id=str(uuid.uuid4()),
            package=data,
            status="Shipped",
            pickup_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=2),
            recipient_name="Cheesedz",
            delivery_address="UET-VNU"
        )

        logging.info(f"Delivery created: {delivery}")
        webHookCallback(delivery)

        return delivery
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def webHookCallback(data: Delivery):
    requests.post(
        url=f"{os.environ.get('BACKEND_URL')}/api/listen",
        json={
            "data": json.dumps(data.model_dump(), default=custom_json_serializer),
            "topic": "notification",
            "status": "done"
        }
    )
    return