# Run Command
#! uvicorn "gateway-service.app.main:app" --reload --host "localhost" --port 8000

import os

from fastapi import APIRouter, FastAPI, Request, Response, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from .fastapi_gateway import route

from .models.goods_models import Good, GoodUpdate
from .models.orders_models import OrderIn, OrderOut, OrderStatus, OrderUpdate
from .models.users_models import UserIn, UserLogin, UserOut
from .api.auth_bearer import JWTBearer

DB_URL = os.environ.get('DB_URL', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'microservices')
APP_NAME = os.environ.get('APP_NAME', 'Gateway API')
GATEWAY_URL = os.environ.get('GATEWAY_URL', 'http://localhost:8000')
GOODS_URL = os.environ.get('GOODS_URL', 'http://localhost:8001')
ORDERS_URL = os.environ.get('ORDERS_URL', 'http://localhost:8002')
USERS_URL = os.environ.get('USERS_URL', 'http://localhost:8003')


users_router = APIRouter()
goods_router = APIRouter()
orders_router = APIRouter()

app = FastAPI(title=APP_NAME)


@app.on_event('startup')
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongodb_client.close()

# Users:
# post create_user(request, user model)
# post user_login(request, user login model)
# get list_users(request) # uses bearer
# get get_user(id, request) # uses bearer
# delete delete_user(id, request) # uses bearer, only for admin


@route(
    request_method=users_router.post,
    service_url=USERS_URL,
    gateway_path='/users/sign_up',
    service_path='/v1/users/sign_up',
    response_model=None,
    query_params=None,
    body_params=['user'],
    dependencies=None,
    response_description='Create a user'
)
async def create_user(request: Request, user: UserIn, response: Response):
    pass


@route(
    request_method=users_router.post,
    service_url=USERS_URL,
    gateway_path='/users/login',
    service_path='/v1/users/login',
    response_model=None,
    query_params=None,
    body_params=['user'],
    dependencies=None,
    response_description='Login user'
)
async def user_login(request: Request, user: UserLogin, response: Response):
    pass


@route(
    request_method=users_router.get,
    service_url=USERS_URL,
    gateway_path='/users',
    service_path='/v1/users/',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='List of all users'
)
async def list_users(request: Request, response: Response):
    pass


@route(
    request_method=users_router.get,
    service_url=USERS_URL,
    gateway_path='/users/{id}',
    service_path='/v1/users/{id}',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Get user by id'
)
async def get_user(id: str, request: Request, response: Response):
    pass


@route(
    request_method=users_router.delete,
    service_url=USERS_URL,
    gateway_path='/users/{id}',
    service_path='/v1/users/{id}',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Delete user by id'
)
async def delete_user(id: str, request: Request, response: Response):
    pass

# Goods:
#! All actions on goods use JWTBearer
# post add_good(request, good model)
# get list_goods(request)
# get show_good(id, request)
# put update_good(id, request, update good model)
# delete delete_good(id, request)


@route(
    request_method=goods_router.post,
    service_url=GOODS_URL,
    gateway_path='/goods',
    service_path='/v1/goods/',
    response_model=None,
    query_params=None,
    body_params=['good'],
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Add new good'
)
async def add_good(request: Request, good: Good, response: Response):
    pass


@route(
    request_method=goods_router.get,
    service_url=GOODS_URL,
    gateway_path='/goods',
    service_path='/v1/goods/',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=None,
    response_description='List of all goods'
)
async def list_goods(request: Request, response: Response):
    pass


@route(
    request_method=goods_router.get,
    service_url=GOODS_URL,
    gateway_path='/goods/{id}',
    service_path='/v1/goods/{id}',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=None,
    response_description='Get a single good'
)
async def get_good(id: str, request: Request, response: Response):
    pass


@route(
    request_method=goods_router.put,
    service_url=GOODS_URL,
    gateway_path='/goods/{id}',
    service_path='/v1/goods/{id}',
    response_model=None,
    query_params=None,
    body_params=['good'],
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Update a good'
)
async def update_good(id: str, request: Request, good: GoodUpdate, response: Response):
    pass


@route(
    request_method=goods_router.delete,
    service_url=GOODS_URL,
    gateway_path='/goods/{id}',
    service_path='/v1/goods/{id}',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Delete a good'
)
async def delete_good(id: str, request: Request, response: Response):
    pass


# Orders:
# post make_order(request, order)
# get get_user_orders(request)
@route(
    request_method=orders_router.post,
    service_url=ORDERS_URL,
    gateway_path='/orders',
    service_path='/v1/orders/',
    response_model=None,
    query_params=None,
    body_params=['order'],
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Make new order'
)
async def make_order(order: OrderIn, request: Request, response: Response):
    pass

@route(
    request_method=orders_router.get,
    service_url=ORDERS_URL,
    gateway_path='/orders',
    service_path='/v1/orders/',
    response_model=None,
    query_params=None,
    body_params=None,
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Get all orders by user'
)
async def get_user_orders(request: Request, response: Response):
    pass

@route(
    request_method=orders_router.put,
    service_url=ORDERS_URL,
    gateway_path='/orders/{id}',
    service_path='/v1/orders/{id}',
    response_model=None,
    query_params=None,
    body_params=['changed_order'],
    dependencies=[
        Depends(JWTBearer())
    ],
    response_description='Update existing order'
)
async def update_order(id: str, changed_order: OrderUpdate, request: Request, response: Response):
    pass

app.include_router(users_router, tags=['users'])
app.include_router(goods_router, tags=['goods'])
app.include_router(orders_router, tags=['orders'])
