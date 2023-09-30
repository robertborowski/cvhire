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
    'Home': '/home',
    'CVs & Resumes': '/cv',
    'Roles': '/roles',
    'Results': '/results',
    'Export': '/export'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def navbar_link_dict_function_v2():
  output_dict = {
    'Help': {
      'icon':'fa-solid fa-circle-question',
      'url':'/help'
    },
    'Notifications': {
      'icon':'fa-solid fa-bell',
      'url':'/notifications'
    },
    'Settings': {
      'icon':'fa-solid fa-gear',
      'url':'/settings'
    },
    'Account': {
      'icon':'fa-solid fa-user',
      'url':'/account'
    }
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_roles_function():
  output_dict = {
    'Open': '/roles/open',
    'Filled': '/roles/filled',
    'Archived': '/roles/archive',
    'All roles': '/roles/all'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_cv_function():
  output_dict = {
    'Active': '/cv/active',
    'Archived': '/cv/archive',
    'All CVs': '/cv/all'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def role_status_codes_function():
  arr = ['open','filled','archive','all','delete']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def cv_status_codes_function():
  arr = ['active','archive','all','delete']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def ai_status_codes_function():
  arr = ['one-role-many-cvs','one-cv-many-roles']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def roles_table_links_function(role_type):
  output_dict = {}
  # ------------------------ type start ------------------------
  if role_type == 'open':
    output_dict = {
      'Edit role': {
        'icon':'fa-solid fa-pen-to-square',
        'url':'/roles/edit'
      },
      'Move to filled': {
        'icon':'fa-regular fa-square-minus',
        'url':'/roles/status/filled'
      },
      'Move to archive': {
        'icon':'fa-solid fa-square-xmark',
        'url':'/roles/status/archive'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'filled':
    output_dict = {
      'Edit role': {
        'icon':'fa-solid fa-pen-to-square',
        'url':'/roles/edit'
      },
      'Move to open': {
        'icon':'fa-regular fa-square-check',
        'url':'/roles/status/open'
      },
      'Move to archive': {
        'icon':'fa-solid fa-square-xmark',
        'url':'/roles/status/archive'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'archive':
    output_dict = {
      'Edit role': {
        'icon':'fa-solid fa-pen-to-square',
        'url':'/roles/edit'
      },
      'Move to open': {
        'icon':'fa-regular fa-square-check',
        'url':'/roles/status/open'
      },
      'Move to filled': {
        'icon':'fa-regular fa-square-minus',
        'url':'/roles/status/filled'
      },
      'Delete role': {
        'icon':'fa-solid fa-trash',
        'url':'/roles/status/delete'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'all':
    output_dict = {
      'Edit role': {
        'icon':'fa-solid fa-pen-to-square',
        'url':'/roles/edit'
      }
    }
  # ------------------------ type end ------------------------
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def cv_table_links_function(role_type):
  output_dict = {}
  # ------------------------ type start ------------------------
  if role_type == 'active':
    output_dict = {
      'Move to archive': {
        'icon':'fa-solid fa-square-xmark',
        'url':'/cv/status/archive'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'archive':
    output_dict = {
      'Move to active': {
        'icon':'fa-regular fa-square-check',
        'url':'/cv/status/active'
      },
      'Delete CV': {
        'icon':'fa-solid fa-trash',
        'url':'/cv/status/delete'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'all':
    output_dict = {
      # 'Edit role': {
      #   'icon':'fa-solid fa-pen-to-square',
      #   'url':'/roles/edit'
      # }
    }
  # ------------------------ type end ------------------------
  return output_dict
# ------------------------ individual function end ------------------------
