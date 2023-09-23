
# ------------------------ imports start ------------------------

import redis
import os
from flask import request
from website.backend.uuid import create_uuid_function, create_timestamp_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def redis_connect_to_database_function():
  try:
    # Connecting to Redis pool method
    pool = redis.ConnectionPool(
      host = os.environ.get('CVHIRE_REDIS_HOST_NAME'),
      port = str(os.environ.get('CVHIRE_REDIS_PORT')),
      password = os.environ.get('CVHIRE_REDIS_PASSWORD'),
      db=0)
    #redis_connection = redis.Redis(connection_pool=pool)
    redis_connection = redis.StrictRedis(connection_pool=pool)
  except:
    print('redis connection failed!')
    return 'redis connection failed!'
  # Return the connection
  return redis_connection
# ------------------------ individual function end ------------------------


# ------------------------ individual function start ------------------------
def redis_check_if_cookie_exists_function():
  try:
    get_cookie_value_from_browser = request.cookies.get('user_candidates_browser_cookie')
  except:
    get_cookie_value_from_browser = None
  return get_cookie_value_from_browser
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_check_if_employees_cookie_exists_function():
  try:
    get_cookie_value_from_browser = request.cookies.get('user_employees_browser_cookie')
  except:
    get_cookie_value_from_browser = None
  return get_cookie_value_from_browser
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_set_browser_cookie_function():
  set_browser_cookie_key = 'user_candidates_browser_cookie'
  set_browser_cookie_value = create_uuid_function('bcooke_')
  return set_browser_cookie_key, set_browser_cookie_value
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_set_employees_browser_cookie_function():
  set_browser_cookie_key = 'user_employees_browser_cookie'
  set_browser_cookie_value = create_uuid_function('b2cooke_')
  return set_browser_cookie_key, set_browser_cookie_value
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_logout_all_other_signins_function(input_id):
  try:
    # ------------------------ connect to redis start ------------------------
    redis_connection = redis_connect_to_database_function()
    redis_keys = redis_connection.keys()
    # ------------------------ connect to redis end ------------------------
    # ------------------------ loop through start ------------------------
    for key in redis_keys:
      redis_value = redis_connection.get(key).decode('utf-8')
      if redis_value == input_id:
        redis_connection.delete(key.decode('utf-8'))
    # ------------------------ loop through end ------------------------
  except:
    pass
  return True
# ------------------------ individual function start ------------------------