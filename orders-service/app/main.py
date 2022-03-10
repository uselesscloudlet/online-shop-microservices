# Run Command
#! uvicorn "orders-service.app.main:app" --reload --host "localhost" --port 8002

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os

from .api.router import router as orders_router

DB_URL = os.environ.get('DB_URL', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'microservices')
APP_NAME = os.environ.get('APP_NAME', 'Orders API')


app = FastAPI(title=APP_NAME)


@app.on_event('startup')
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(orders_router, tags=['orders'], prefix='/v1/orders')