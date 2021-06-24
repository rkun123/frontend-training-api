from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from middlewares.auth import get_current_user
from typing import List, Optional
from cruds import createPost, createThread, getThread, listPosts, listThread, deletePost
from schemas import CreatePostPayload, Thread, CreateThreadPayload, Post, User

r = APIRouter()

# post
@r.post('/posts', response_model=Post)
async def create_post(payload: CreatePostPayload, user: User = Depends(get_current_user)):
  if user == None:
    raise HTTPException(401, 'Token decode error')

  thread = getThread(payload.thread_key)
  if thread == None:
    raise HTTPException(404, 'Thread not found')

  return createPost(payload, user)

@r.get('/threads/{thread_key}/posts', response_model=List[Post])
async def list_posts(limit: int = 10, page: int = 1, thread_key: str = ''):
  thread = getThread(thread_key)
  if thread == None:
    raise HTTPException(404, 'Thread not found')
  posts = listPosts(thread, limit=limit, page=page)
  return posts

@r.delete('/posts/{post_key}')
async def delete_post(post_key: str = '', user: User = Depends(get_current_user)):
  if user == None:
    raise HTTPException(401, 'Token decode error')

  deletePost(post_key, user)
