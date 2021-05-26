from fastapi import Header
from jwt_token import decodeToken
from typing import Union
from schemas import User

# (Must be authorized) get current user
def get_current_user(jwt_token: str = Header(None)) -> Union[User, None]:
  print('authorization: ', jwt_token)
  try:
    token = jwt_token.split(' ')[1]
    user = decodeToken(token)
    return user

  except Exception as e:
    return None
