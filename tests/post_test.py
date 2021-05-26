from main import app
from fastapi.testclient import TestClient
from .utils import random_str

client = TestClient(app)

def signin() -> str:
  payload = {
    'email': 'example@example.com',
    'password': 'password'
  }
  res = client.post('/api/v1/auth/signin', json=payload)
  return res.json()['jwt']


def test_create_post():
  token = signin()
  print('token', token)
  payload = {
    'content': random_str(15),
    'thread_key': 'g9660u8pwlwe'
  }
  res = client.post('/api/v1/posts', json=payload, headers={'jwt-token': "Bearer {}".format(token)})

  print(res.json())
  assert res.status_code == 200
  assert res.json()['content'] == payload['content']

def test_create_post_to_non_existing_thread_should_be_rejected():
  token = signin()
  print('token', token)
  payload = {
    'content': random_str(15),
    'thread_key': 'hogefuga' # Non exist thread key
  }
  res = client.post('/api/v1/posts', json=payload, headers={'jwt-token': "Bearer {}".format(token)})

  assert res.status_code == 404

def test_create_post_without_auth_token_should_be_rejected():
  payload = {
    'content': random_str(15),
    'thread_key': 'g9660u8pwlwe'
  }
  res = client.post('/api/v1/posts', json=payload)

  print(res.json())
  assert res.status_code == 401

def test_list_posts():
  res = client.get("/api/v1/threads/{}/posts".format('g9660u8pwlwe'))

  assert res.status_code == 200
  posts = res.json()
  print(res.json())
  assert len(posts) >= 1
