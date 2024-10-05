from dotenv import load_dotenv
import os, requests, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Package, Payment
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

@app.post('/api/package')
async def createPackge(data: Payment):
    package = Package(
        package_id=str(uuid.uuid4()),  
        order_id=data.order.order_id, 
        weight=2.5, 
        dimensions="10x5x2",  
        packaging_type="Box",  
        shipped_date=datetime.now(),
        expected_delivery_date=datetime.now() + timedelta(days=random.randint(1, 10)), 
        current_status="Shipped",  
        tracking_number="ABC123456789",  
        courier_service="DHL"  
    )

    logging.info(f"Package created: {package}")

    webHookCallback(package)
    return package

def webHookCallback(data: Package):
    requests.post(
        url=f"{os.environ.get('BACKEND_URL')}/api/listen",
        json={
            "data": json.dumps(data.model_dump(), default=custom_json_serializer),
            "topic": "package",
            "status": "done"
        }
    )
    return