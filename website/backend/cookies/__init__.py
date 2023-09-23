# ------------------------ imports start ------------------------
from flask import request
from flask import Blueprint, render_template, request, make_response
import datetime
from website.backend.uuid_timestamp import create_uuid_function
from website.backend.connection import redis_connect_open_function
# ------------------------ imports end ------------------------

# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual function start ------------------------
def redis_check_if_cookie_exists_function():
  try:
    get_cookie_value_from_browser = request.cookies.get('cvhire_user_browser_cookie')
  except:
    get_cookie_value_from_browser = None
  return get_cookie_value_from_browser
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function(current_user, input_template_url, page_dict):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function('login')
  browser_response = make_response(render_template(input_template_url, user=current_user, page_dict_html=page_dict))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def redis_set_browser_cookie_function(input_code):
  if input_code == 'login':
    set_browser_cookie_key = 'cvhire_user_browser_cookie'
    set_browser_cookie_value = create_uuid_function('bcooke_')
  return set_browser_cookie_key, set_browser_cookie_value
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_logout_all_other_signins_function(input_id):
  try:
    # ------------------------ connect to redis start ------------------------
    redis_connection = redis_connect_open_function()
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