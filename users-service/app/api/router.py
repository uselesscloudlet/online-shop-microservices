from fastapi import APIRouter, Body, Request, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from passlib.hash import pbkdf2_sha256
import pymongo
import itertools

from .models import UserIn, UserLogin, UserOut
from .auth_handler import signJWT, decodeJWT

router = APIRouter()


async def check_user(request: Request, data: UserIn, only_email: bool = False):
    user_from_db = await request.app.mongodb['users'].find_one({'email': data.email})
    if only_email:
        if user_from_db:
            return True
    else:
        if user_from_db is not None and pbkdf2_sha256.verify(data.password, user_from_db['password']):
            return True
    return False


@router.post('/sign_up', response_description='Create new user')
async def create_user(request: Request, user: UserIn = Body(...)):
    if not await check_user(request, user, True):
        user = jsonable_encoder(user)
        user['password'] = pbkdf2_sha256.hash(user['password'])
        await request.app.mongodb['users'].insert_one(user)
        return signJWT(user['email'])

    return JSONResponse(status_code=status.HTTP_226_IM_USED, content='This email or username is busy')


@router.post('/login', response_description='Login user')
async def user_login(request: Request, user: UserLogin = Body(...)):
    if await check_user(request, user):
        user = jsonable_encoder(user)
        return signJWT(user['email'])

    raise HTTPException(
        status_code=404, detail=f'User with this email({user.email}) not found or you have used wrong password')


@router.get('/', response_description='List of all users')
async def list_users(request: Request):
    users_list = []
    users = await request.app.mongodb['users'].find().sort('username', pymongo.ASCENDING).to_list(None)
    for user in users:
        users_list.append(
            {'user_id': user['_id'], 'username': user['username']}
        )

    return users_list


@router.get('/{id}', response_description='Get user by id')
async def get_user(id: str, request: Request):
    if user := await request.app.mongodb['users'].find_one({'_id': id}):
        return dict(itertools.islice(user.items(), 4))

    raise HTTPException(status_code=404, detail=f'User with id {id} not found')

@router.delete('/{id}', response_description='Delete user by id')
async def delete_user(id: str, request: Request, response: Response):
    token = request.headers.get('authorization').replace('Bearer ', '')
    email = decodeJWT(token)['user_email']
    user = await request.app.mongodb['users'].find_one({'email': email})
    if user['user_type'] in ['admin']:
        delete_result = await request.app.mongodb['users'].delete_one({'_id': id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_200_OK)
    
        raise HTTPException(status_code=404, detail=f'Good with id {id} not found')
    else:
        raise HTTPException(status_code=403, detail='You have no rights for this action')

