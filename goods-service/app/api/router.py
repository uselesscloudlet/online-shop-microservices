from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import Good, GoodUpdate
from .auth_handler import decodeJWT

router = APIRouter()


@router.post('/', response_description='Add new good')
async def add_good(request: Request, good: Good = Body(...)):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    if user['user_type'] in ['admin', 'manager']:

        good = jsonable_encoder(good)
        new_good = await request.app.mongodb['goods'].insert_one(good)
        created_good = await request.app.mongodb['goods'].find_one(
            {'_id': new_good.inserted_id}
        )

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_good)
    else:
        raise HTTPException(
            status_code=403, detail='You have no rights for this action')


@router.get('/', response_description='List of all goods')
async def list_goods(request: Request):
    goods = []
    for good in await request.app.mongodb['goods'].find().to_list(None):
        goods.append(good)

    return goods


@router.get('/{id}', response_description='Get a single good')
async def get_good(id: str, request: Request):
    if good := await request.app.mongodb['goods'].find_one({'_id': id}):
        return good

    raise HTTPException(status_code=404, detail=f'Good with id {id} not found')


@router.put('/{id}', response_description='Update a good')
async def update_good(id: str, request: Request, good: GoodUpdate = Body(...)):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    if user['user_type'] in ['admin', 'manager']:
        good = {k: v for k, v in good.dict().items() if v is not None}

        if len(good) >= 1:
            update_result = await request.app.mongodb['goods'].update_one(
                {'_id': id}, {'$set': good}
            )

            if update_result.modified_count == 1:
                if updated_good := await request.app.mongodb['goods'].find_one({'_id': id}) is not None:
                    return updated_good

        if existing_good := await request.app.mongodb['goods'].find_one({'_id': id}) is not None:
            return existing_good

        raise HTTPException(
            status_code=404, detail=f'Good with id {id} not found')
    else:
        raise HTTPException(
            status_code=403, detail='You have no rights for this action')


@router.delete('/{id}', response_description='Delete good')
async def delete_good(id: str, request: Request):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    if user['user_type'] in ['admin', 'manager']:
        delete_result = await request.app.mongodb['goods'].delete_one({'_id': id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_200_OK)

        raise HTTPException(
            status_code=404, detail=f'Good with id {id} not found')
    else:
        raise HTTPException(
            status_code=403, detail='You have no rights for this action')
