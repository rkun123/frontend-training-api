import types
from deta import Deta
from fastapi import HTTPException
from schemas import CreatePostPayload, CreateThreadPayload, Post, User, SigninPayload, SignupPayload, Thread
from uuid import uuid4
from more_itertools import ilen
from datetime import datetime
from typing import List, Optional
import jwt
import bcrypt
import os

# project key
deta = Deta(os.environ.get('DETA_TOKEN', 'c01jifyn_JnRrTsxwQmg7Uzw8beRTJN7CowUNhKQB'))
userDB = deta.Base('users')
threadDB = deta.Base('threads')
postDB = deta.Base('posts')

salt = os.environ.get('PASSWORD_HASH_SALT', '$2a$10$ThXfVCPWwXYx69U8vuxSUu').encode()

def genID():
  return str(uuid4())

def genPasswordHash(password: str):
  hash = bcrypt.hashpw(password.encode(), salt)
  return hash.decode()

def createUser(signupPayload: SignupPayload) -> User:
  id = genID()
  password_hash = genPasswordHash(signupPayload.password)
  user = User(
    email=signupPayload.email,
    name=signupPayload.name,
    description=signupPayload.description,
    password_hash=password_hash,
  )
  users = list(userDB.fetch({ 'email': signupPayload.email }))[0]
  if len(users) >= 1:
    raise HTTPException(status_code=400, detail='Already exists user has same email')

  res = userDB.put(user.dict(), key=id)
  res_user = User(
    key=res['key'],
    email=res['email'],
    name=res['name'],
    description=res['description'],
    created_at=res['created_at'],
    updated_at=res['created_at']
  )
  print(res_user)
  return res_user

def getUserByEmail(email: str) -> User:
  users = list(userDB.fetch({ 'email': email }))[0]
  if len(users) <= 0:
    print('User not found by email')
    raise HTTPException(status_code=401, detail='User not found')
  
  return User(**users[0])

def getUserById(key: str) -> User:
  users = list(userDB.fetch(key))[0]
  if len(users) >= 1:
    raise HTTPException(status_code=401, detail='User not found')
  
  return User(**users[0])

# Threads

def createThread(payload: CreateThreadPayload, user: User) -> Thread:
  threads = list(threadDB.fetch({ 'name': payload.name }))[0]
  if len(threads) >= 1:
    raise HTTPException(status_code=400, detail='Already exists thread has same name')
  
  thread = Thread(
    name = payload.name,
    author_key = user.key
  )
  
  thread_dict = threadDB.put(thread.dict(exclude_none=True))
  return Thread(**thread_dict)

def getThread(key: str) -> Optional[Thread]:
  thread_dict = threadDB.get(key)
  if thread_dict == None:
    return None
  thread = Thread(**thread_dict)
  return thread

def listThread(limit: int = 10, page: int = 1) -> List[Thread]:
  thread_iter = threadDB.fetch(pages=page, buffer=limit)
  thread_dicts = []
  for i in range(page):
    try:
      thread_dicts = next(thread_iter)
    except StopIteration:
      raise HTTPException(status_code=404, detail='specified page is out of range')
  
  threads = list(map(lambda t: Thread(**t), thread_dicts))
  return threads

def createPost(payload: CreatePostPayload, user: User) -> Post:
  post = Post(author_key=user.key, **payload.dict(exclude_none=True))
  post_dict = postDB.put(post.dict(exclude_none=True))
  post = Post(**post_dict)
  return post
  
def listPosts(thread: Thread, limit: int = 10, page: int = 1) -> List[Post]:
  post_iter = postDB.fetch({ 'thread_key': thread.key }, pages=page, buffer=limit)
  post_dicts = []
  for i in range(page):
    try:
      post_dicts = next(post_iter)
    except StopIteration:
      raise HTTPException(status_code=404, detail='specified page is out of range')
  
  posts = list(map(lambda t: Post(**t), post_dicts))
  return posts