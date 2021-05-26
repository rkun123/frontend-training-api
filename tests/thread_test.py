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


def test_create_thread():
  token = signin()
  payload = {
    'name': "test_thread.{}".format(random_str(5))
  }
  res = client.post('/api/v1/threads', json=payload, headers={'jwt-token': "Bearer {}".format(token)})

  print(res.json())
  assert res.status_code == 200
  print(res.json())

def test_create_thread_without_auth_token_should_be_rejected():
  token = signin()
  payload = {
    'name': "test_thread.{}".format(random_str(5))
  }
  res = client.post('/api/v1/threads', json=payload)
  print(res.json())
  assert res.status_code == 401

def test_list_thread():
  token = signin()
  res = client.get('/api/v1/threads', headers={'jwt-token': "Bearer {}".format(token)})

  assert res.status_code == 200
  threads = res.json()
  print(res.json())
  assert len(threads) >= 1
  assert len(threads) <= 10



  