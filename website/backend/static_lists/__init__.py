# ------------------------ imports start ------------------------
from website.models import EmailBlockObj
from website import db
from website.backend.connection import redis_connect_open_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_list_function(list_name):
  if list_name == None:
    return None
  if list_name == 'blocked_email_arr':
    db_objs = EmailBlockObj.query.all()
    arr = []
    for i in db_objs:
      arr.append(i.id)
    # arr = ['@gartner.com','@gmail.com','@gmail','@yahoo.','@ymail.com','@mail.com','@msn.','@aol.','@fb.com','@hotmail.','@outlook.','@topmail.ws','@iopmail.com','@mailinator.com','@onmicrosoft.com','@bingzone.net','@msgsafe.io','@sharklasers.com','@ttirv.com','@pm.me','@protonmail.com','@qq.com','@gamil.com','@gmal.com','@me.com','@yopmail.com','@hey.com','@icloud.com','@fastmail.fm','@mail.ru','@web.de','@ya.ru','@vp.pl','@inboxbear.com','@tuks.co.za','@kiabws.com','@cikuh.com','@relay.firefox.com','@citromail.hu','@mailpoof.com','@biyac.com','@byom.de','@yandex.ru','@naver.com','@ukr.net','@cuoly.com','@zohomail.in','@sltn.net','@laposte.sn','.edu']
    return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def redis_all_keys_function():
  redis_keys = None
  try:
    redis_connection = redis_connect_open_function()
    redis_keys = redis_connection.keys()
  except:
    pass
  return redis_keys
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def navbar_link_dict_function():
  output_dict = {
    'Home': 'home',
    'CVs & Resumes': 'cv',
    'Roles': 'roles',
    'Favorites': 'favorites',
    'Export': 'export'
  }
  return output_dict
# ------------------------ individual function end ------------------------
