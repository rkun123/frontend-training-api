import jwt
from fastapi import HTTPException
from schemas import SigninPayload, User
from cruds import getUserByEmail, genPasswordHash
from datetime import datetime, timedelta
import os

SECRET = os.environ.get('SECRET', 'jwt_secret')

def generateToken(payload: SigninPayload) -> str:
  user = getUserByEmail(email=payload.email)
  password_hash = genPasswordHash(payload.password)
  if user.password_hash != password_hash:
    raise HTTPException(status_code=401, detail='Password is not correct')

  jwt_payload = {
    'exp': datetime.utcnow() + timedelta(10),
    'user': user.dict()
  }

  encoded_jwt = jwt.encode(jwt_payload, SECRET, algorithm='HS256')
  return encoded_jwt

def decodeToken(token: str) -> User:
  user_dict = jwt.decode(token, SECRET, algorithms=['HS256'])
  user = User(**user_dict['user'])
  return user