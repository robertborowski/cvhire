# ------------------------ imports start ------------------------
from website.models import EmailBlockObj, CompanyInfoObj
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
    'Home': '/ai',
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
      'url':'/account/settings'
    },
    'Account': {
      'icon':'fa-solid fa-user',
      'url':'/account/user'
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
def dashboard_section_links_dict_results_function():
  output_dict = {
    'Valid': '/results/valid',
    'Archived': '/results/archive'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_ai_function():
  output_dict = {
    'One role + many CVs': '/ai/one-role-many-cvs',
    'One CV + many roles': '/ai/one-cv-many-roles',
    'CV ask AI': '/cv/active'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_export_function():
  output_dict = {
    'Results': '/export/export_results'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_help_function():
  output_dict = {
    'Request': '/help/request'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_notifications_function():
  output_dict = {
    'Unread': '/notifications/unread',
    'Read': '/notifications/read'
  }
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_section_links_dict_account_function():
  output_dict = {
    'User': '/account/user',
    'Settings': '/account/settings'
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
def results_status_codes_function():
  arr = ['valid','archive','delete']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def export_status_codes_function():
  arr = ['export_results']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def help_status_codes_function():
  arr = ['request']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def notifications_status_codes_function():
  arr = ['unread','read']
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def account_status_codes_function():
  arr = ['user','settings']
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

# ------------------------ individual function start ------------------------
def results_table_links_function(role_type):
  output_dict = {}
  # ------------------------ type start ------------------------
  if role_type == 'valid':
    output_dict = {
      'Move to archive': {
        'icon':'fa-solid fa-square-xmark',
        'url':'/results/status/archive'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'archive':
    output_dict = {
      'Move to valid': {
        'icon':'fa-regular fa-square-check',
        'url':'/results/status/valid'
      },
      'Delete result': {
        'icon':'fa-solid fa-trash',
        'url':'/results/status/delete'
      }
    }
  # ------------------------ type end ------------------------
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def notifications_table_links_function(role_type):
  output_dict = {}
  # ------------------------ type start ------------------------
  if role_type == 'unread':
    output_dict = {
      'Mark as read': {
        'icon':'fa-solid fa-check',
        'url':'/notifications/status/read'
      }
    }
  # ------------------------ type end ------------------------
  # ------------------------ type start ------------------------
  elif role_type == 'read':
    output_dict = {
      'Mark as unread': {
        'icon':'fa-solid fa-x',
        'url':'/notifications/status/unread'
      }
    }
  # ------------------------ type end ------------------------
  return output_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_stars_img_function(i_dict):
  i_dict['score_all_stars'] = ''
  if float(i_dict['score']) >= 4.51:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_5.png'
  elif float(i_dict['score']) >= 4.5:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_4_half.png'
  elif float(i_dict['score']) >= 4.0:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_4.png'
  elif float(i_dict['score']) >= 3.5:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_3_half.png'
  elif float(i_dict['score']) >= 3.0:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_3.png'
  elif float(i_dict['score']) >= 2.5:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_2_half.png'
  elif float(i_dict['score']) >= 2.0:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_2.png'
  elif float(i_dict['score']) >= 1.5:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_1_half.png'
  elif float(i_dict['score']) >= 1.0:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_1.png'
  elif float(i_dict['score']) >= 0.5:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_0_half.png'
  elif float(i_dict['score']) >= 0.0:
    i_dict['score_all_stars'] = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_0.png'
  return i_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_stars_img_dict_function():
  i_dict = {
    '0': {
      'id': '0',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_0.png',
      'num': '0.0'
    },
    '0half': {
      'id': '0half',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_0_half.png',
      'num': '0.5'
    },
    '1': {
      'id': '1',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_1.png',
      'num': '1.0'
    },
    '1half': {
      'id': '1half',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_1_half.png',
      'num': '1.5'
    },
    '2': {
      'id': '2',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_2.png',
      'num': '2.0'
    },
    '2half': {
      'id': '2half',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_2_half.png',
      'num': '2.5'
    },
    '3': {
      'id': '3',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_3.png',
      'num': '3.0'
    },
    '3half': {
      'id': '3half',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_3_half.png',
      'num': '3.5'
    },
    '4': {
      'id': '4',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_4.png',
      'num': '4.0'
    },
    '4half': {
      'id': '4half',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_4_half.png',
      'num': '4.5'
    },
    '5': {
      'id': '5',
      'url': 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/all_stars_5.png',
      'num': '5.0'
    }
  }
  i_arr = ['0.0','0.5','1.0','1.5','2.0','2.5','3.0','3.5','4.0','4.5','5.0']
  return i_dict, i_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_default_profile_imgs_function():
  img_dict = {
    'Green': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_green.png',
      'id': '1'
    },
    'Black': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_black.png',
      'id': '2'
    },
    'Blue': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_blue.png',
      'id': '3'
    },
    'Orange': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_orange.png',
      'id': '4'
    },
    'Purple': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_purple.png',
      'id': '5'
    },
    'Red': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_red.png',
      'id': '6'
    },
    'White': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_white.png',
      'id': '7'
    },
    'Yellow': {
      'url':'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_yellow.png',
      'id': '8'
    }
  }
  return img_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_keyword_colors_function(i_keyword):
  html_bg_color = 'custom-bg-primary'
  html_text_color = 'custom-color-black'
  if i_keyword.lower() == 'hiring success':
    html_bg_color = 'custom-bg-success'
    html_text_color = 'custom-color-white'
  if i_keyword.lower() == 'resume parsing':
    html_bg_color = 'custom-bg-primary'
    html_text_color = 'custom-color-black'
  if i_keyword.lower() == 'ai':
    html_bg_color = 'custom-bg-info'
    html_text_color = 'custom-color-black'
  if i_keyword.lower() == 'applicant tracking system' or i_keyword.lower() == 'ats':
    html_bg_color = 'custom-bg-danger'
    html_text_color = 'custom-color-white'
  else:
    pass
  return html_bg_color, html_text_color
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_companies_function():
  arr = []
  db_objs = CompanyInfoObj.query.filter_by(active=True).all()
  for i_obj in db_objs:
    arr.append(i_obj.name)
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_special_chars_function():
  chars_dict = {
    "'": "",
    '.': '',
    'á': 'a',
    'ë': 'e',
    'ć': 'c',
    'ü': 'u',
    "’": '',
    '(': '',
    ')': '',
    '[': '',
    ']': '',
    '"': '',
    '-': ' '
  }
  return chars_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_linkedin_identifiers_function():
  arr = [
    'she/her/hers',
    'she/her/ella',
    'she/her',
    'they/he',
    'he/him',
    'shrm cp'
  ]
  return arr
# ------------------------ individual function end ------------------------
