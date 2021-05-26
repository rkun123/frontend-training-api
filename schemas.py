from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

def now_timestamp() -> float:
  return datetime.now().timestamp()

class User(BaseModel):
  key: Optional[str]
  name: str
  email: str
  description: str
  created_at: float = Field(default_factory=now_timestamp)
  updated_at: float = Field(default_factory=now_timestamp)
  key: Optional[str]
  password_hash: Optional[str]

class CreateThreadPayload(BaseModel):
  name: str

class Thread(BaseModel):
  key: Optional[str]
  name: str
  author_key: str
  created_at: float = Field(default_factory=now_timestamp)
  updated_at: float = Field(default_factory=now_timestamp)

class CreatePostPayload(BaseModel):
  thread_key: str
  content: str

class Post(BaseModel):
  key: Optional[str]
  author_key: str
  thread_key: str
  content: str
  created_at: float = Field(default_factory=now_timestamp)
  updated_at: float = Field(default_factory=now_timestamp)

class SignupPayload(BaseModel):
  name: str
  email: str
  password: str
  description: str

class SignupResponse(BaseModel):
  name: str
  email: str
  password_hash: str
  description: str

class SigninPayload(BaseModel):
  email: str
  password: str