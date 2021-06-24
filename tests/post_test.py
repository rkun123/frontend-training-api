from uuid import uuid4
from main import app
from fastapi.testclient import TestClient
from .utils import create_post, get_random_thread, random_str, sign_in, create_random_thread

client = TestClient(app)

def test_create_post():
  token = sign_in()
  thread = create_random_thread(token)
  payload = {
    'content': random_str(15),
    'thread_key': thread.key
  }
  res = client.post('/api/v1/posts', json=payload, headers={'jwt-token': "Bearer {}".format(token)})

  print(res.json())
  assert res.status_code == 200
  assert res.json()['content'] == payload['content']

def test_create_post_to_non_existing_thread_should_be_rejected():
  token = sign_in()
  print('token', token)
  payload = {
    'content': random_str(15),
    'thread_key': str(uuid4()) # Non exist thread key
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
  thread = get_random_thread()
  create_post(thread.key)
  res = client.get(f'/api/v1/threads/{thread.key}/posts')

  assert res.status_code == 200
  posts = res.json()
  print(res.json())
  assert len(posts) >= 1

def test_delete_posts():
  token = sign_in()
  thread = create_random_thread(token)
  post = create_post(thread_key=thread.key)
  post = create_post(thread_key=thread.key)

  res = client.get(f'/api/v1/threads/{thread.key}/posts')

  assert res.status_code == 200

  assert len(res.json()) == 2

  res = client.delete(f'/api/v1/posts/{post.key}', headers={'jwt-token': "Bearer {}".format(token)})

  assert res.status_code == 200

  res = client.get(f'/api/v1/threads/{thread.key}/posts')

  assert res.status_code == 200

  posts = res.json()

  assert len(posts) == 1


def test_delete_unowned_posts_should_be_rejected():
  token = sign_in()
  another_user_token = sign_in(email='test2@example.com', password='testpassword2')
  thread = create_random_thread(token)
  post = create_post(thread_key=thread.key)
  post = create_post(thread_key=thread.key)

  res = client.get(f'/api/v1/threads/{thread.key}/posts')

  assert res.status_code == 200

  assert len(res.json()) == 2

  res = client.delete(f'/api/v1/posts/{post.key}', headers={'jwt-token': "Bearer {}".format(another_user_token)})

  assert res.status_code == 401

  res = client.get(f'/api/v1/threads/{thread.key}/posts')

  assert res.status_code == 200

  posts = res.json()

  assert len(posts) == 2
