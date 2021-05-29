from fastapi import APIRouter
from typing import List, Dict
from schemas import SignupPayload, SigninPayload, Thread, UserWithoutPassWord
from cruds import createUser, createThread, listThread
from jwt_token import generateToken

r = APIRouter()

@r.post('/auth/signup')
async def signup(payload: SignupPayload) -> UserWithoutPassWord:
  user = createUser(payload)
  return user

@r.post('/auth/signin')
async def signin(payload: SigninPayload) -> Dict[str, str]:
  return { 'jwt': generateToken(payload) }
