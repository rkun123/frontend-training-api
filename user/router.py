from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List, Dict
from schemas import UserWithoutPassWord, User
from cruds import createUser, createThread, getUserByKey, listThread
from jwt_token import generateToken
from middlewares.auth import get_current_user

r = APIRouter()

@r.post('/users/{user_key}', response_model=UserWithoutPassWord)
async def signup(user_key: str):
  user = getUserByKey(user_key)
  return UserWithoutPassWord(**user.dict())

@r.get('/users/me', response_model=UserWithoutPassWord)
async def create_thread(user: User = Depends(get_current_user)):
  if user == None:
    raise HTTPException(401, 'Token decode error')

  return UserWithoutPassWord(**user.dict())