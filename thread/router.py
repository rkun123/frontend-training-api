from fastapi import APIRouter, Depends, HTTPException
from middlewares.auth import get_current_user
from typing import List
from cruds import createThread, listThread
from schemas import Thread, CreateThreadPayload, User

r = APIRouter()

# thread
@r.post('/threads')
async def create_thread(payload: CreateThreadPayload, user: User = Depends(get_current_user)) -> Thread:
  if user == None:
    raise HTTPException(401, 'Token decode error')

  return createThread(payload, user)

@r.get('/threads')
async def list_thread(limit: int = 10, page: int = 1) -> List[Thread]:
  threads = listThread(limit=limit, page=page)
  return threads