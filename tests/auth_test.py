from main import app
from fastapi.testclient import TestClient
from .utils import random_str

client = TestClient(app)

def test_signup():
  payload = {
    'email': "example{0}@example.com".format(random_str(5)),
    'name': 'rkun',
    'password': 'password',
    'description': 'hogefuga'
  }
  res = client.post('/api/v1/auth/signup', json=payload)

  assert res.status_code == 200
  res_json = res.json()
  assert res_json['email'] == payload['email']
  assert res_json['name'] == payload['name']
  assert res_json['description'] == payload['description']
  assert res_json['password_hash'] == None

def test_duplicated_signup_should_be_rejected():
  payload = {
    'email': "example{0}@example.com".format(random_str(5)),
    'name': 'rkun',
    'password': 'password',
    'description': 'hogefuga'
  }
  res = client.post('/api/v1/auth/signup', json=payload)

  assert res.status_code == 200
  res_json = res.json()
  assert res_json['email'] == payload['email']
  assert res_json['name'] == payload['name']
  assert res_json['description'] == payload['description']
  assert res_json['password_hash'] == None

  # Duplicated
  res = client.post('/api/v1/auth/signup', json=payload)

  assert res.status_code == 400

def test_sign_in():
  payload = {
    'email': "example@example.com",
    'name': 'rkun',
    'password': 'password',
    'description': 'hogefuga'
  }
  print(client.post('/api/v1/auth/signup', json=payload))

  payload = {
    'email': payload['email'],
    'password': payload['password']
  }

  res = client.post('/api/v1/auth/signin', json=payload)

  assert res.status_code == 200
  assert 'jwt' in res.json().keys()



  