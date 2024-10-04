import sys
from dotenv import load_dotenv
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoint import router

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

app.include_router(router, prefix="/api")