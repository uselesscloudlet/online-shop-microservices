from fastapi import APIRouter, Body, Request, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pymongo
import itertools

from .auth_handler import signJWT, decodeJWT
from .models import OrderIn, OrderStatus, OrderUpdate

router = APIRouter()


@router.post('/', response_description='Make new order')
async def make_order(request: Request, order: OrderIn):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    user_id = user['_id']
    order.user_id = user_id
    order = jsonable_encoder(order)
    new_order = await request.app.mongodb['orders'].insert_one(order)
    created_order = await request.app.mongodb['orders'].find_one(
        {'_id': new_order.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)

@router.get('/', response_description='Get all orders by user')
async def get_user_orders(request: Request):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    user_id = user['_id']
    orders_list = []
    orders = await request.app.mongodb['orders'].find({'user_id': user_id}).sort('created_at', pymongo.ASCENDING).to_list(None)
    for order in orders:
        orders_list.append(order)
    
    return orders_list


@router.put('/{id}', response_description='Update order')
async def update_order(id: str, changed_order: OrderUpdate, request: Request):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    if user['user_type'] in ['admin', 'manager']:
        order = {k: v for k, v in changed_order.dict().items()
                 if v is not None}

        if len(order) >= 1:
            update_result = await request.app.mongodb['orders'].update_one(
                {'_id': id}, {'$set': order}
            )

            if update_result.modified_count == 1:
                if updated_order := await request.app.mongodb['orders'].find_one({'_id': id}) is not None:
                    return updated_order

        if existing_order := await request.app.mongodb['orders'].find_one({'_id': id}) is not None:
            return existing_order

        raise HTTPException(
            status_code=404, detail=f'Order with id {id} not found')
    else:
        raise HTTPException(
            status_code=403, detail='You have no rights for this action')
