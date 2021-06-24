import random
import string
from typing import Dict
from fastapi.testclient import TestClient
from main import app
from schemas import Post, Thread

def random_str(n: int = 5):
   randlst = [random.choice(string.ascii_lowercase + string.digits) for i in range(n)]
   return ''.join(randlst)

def get_client():
   client = TestClient(app)
   return client

def create_random_user() -> Dict[str, str]:
   c = get_client()
   email = f'{random_str(5)}@example.com'
   password = f'{random_str(8)}'
   res = c.post('/api/v1/users', json={
      'name': f'test_{random_str()}',
      'email': email,
      'password': password
   })

   if res.status_code == 200:
      return {
         'email': email,
         'password': password
      }

def sign_in(email: str = 'test@example.com', password: str = 'testpassword') -> str:
   c = get_client()

   # create test user
   c.post('/api/v1/auth/signup', json={
      'name': 'test_user',
      'email': email,
      'password': password,
      'description': 'test_description'
   })
   
   res = c.post('/api/v1/auth/signin', json={
      'email': email,
      'password': password
   })
   if res.status_code == 200:
      return res.json()['jwt']

def create_random_thread(token: str) -> Thread:
   c = get_client()
   token = sign_in()

   res = c.post('/api/v1/threads', headers={ 'jwt-token': f'Bearer {token}'}, json={
      'name': f'test_{random_str(5)}_thread'
   })

   if res.status_code == 200:
      thread_dict = res.json()
      print(thread_dict)
      thread = Thread(**thread_dict)
      return thread
  

def get_random_thread() -> Thread:
   c = get_client()
   res = c.get('/api/v1/threads')
   threads = res.json()
   thread = random.choice(threads)
   return Thread(**thread)

def create_post(thread_key: str) -> Post:
   token = sign_in()
   c = get_client()
   res = c.post('/api/v1/posts', headers={ 'jwt-token': f'Bearer {token}'}, json={
      'thread_key': thread_key,
      'content': '[Test] --content--'
   })
   if(res.status_code == 200):
      return Post(**res.json())