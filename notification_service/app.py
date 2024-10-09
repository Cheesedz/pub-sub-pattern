from dotenv import load_dotenv
import os, requests, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Package, Delivery, Payment
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

@app.post('/api/mail_send')
async def sendMail():
    return f"Notification sent via mail"