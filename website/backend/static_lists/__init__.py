# ------------------------ imports start ------------------------
from website.models import EmailBlockObj, CompanyInfoObj, BlogObj
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
  keywords_primary_arr = ['resume parsing','automated resume screening','resume parser online','resume screening software']
  keywords_success_arr = ['hiring success','hiring with ai','candidate matching','recruitment service','sourcing','online resume parser']
  keywords_info_arr = ['ai','ai recruiting','resume parser','resume']
  keywords_danger_arr = ['applicant tracking system','ats','time to hire','applicant tracking software','ats tracking']
  keywords_orange_arr = ['recruiting services','recruiting','resume parsing software','job description']
  keywords_purple_arr = ['tech recruiters','recruitment system','talent acquisition specialist','crm','candidate relationship management']
  # ------------------------ defaults / primary (warning) start ------------------------
  html_bg_color = 'css-bg-primary'
  html_text_color = 'css-color-black'
  # ------------------------ defaults / primary (warning) end ------------------------
  # ------------------------ color arr start ------------------------
  if i_keyword.lower() in keywords_primary_arr:
    html_bg_color = 'css-bg-primary'
    html_text_color = 'css-color-black'
  # ------------------------ color arr end ------------------------
  # ------------------------ color arr start ------------------------
  if i_keyword.lower() in keywords_success_arr:
    html_bg_color = 'css-bg-success'
    html_text_color = 'css-color-white'
  # ------------------------ color arr end ------------------------
  # ------------------------ color arr start ------------------------
  if i_keyword.lower() in keywords_info_arr:
    html_bg_color = 'css-bg-info'
    html_text_color = 'css-color-black'
  # ------------------------ color arr end ------------------------
  # ------------------------ color arr start ------------------------
  if i_keyword.lower() in keywords_danger_arr:
    html_bg_color = 'css-bg-danger'
    html_text_color = 'css-color-white'
  # ------------------------ color arr end ------------------------
  # ------------------------ color arr start ------------------------
  if i_keyword.lower() in keywords_orange_arr:
    html_bg_color = 'css-bg-orange'
    html_text_color = 'css-color-black'
  # ------------------------ color arr end ------------------------
  # ------------------------ color arr start ------------------------
  if i_keyword.lower() in keywords_purple_arr:
    html_bg_color = 'css-bg-purple'
    html_text_color = 'css-color-white'
  # ------------------------ color arr end ------------------------
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
def get_blog_posts_function():
  return BlogObj.query.filter_by(status=True).order_by(BlogObj.created_timestamp.desc()).limit(6).all()
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_special_chars_function():
  chars_dict = {
    "'": "",
    '.': '',
    'ã': 'a',
    'á': 'a',
    'ć': 'c',
    'ë': 'e',
    'é': 'e',
    'è': 'e',
    'ñ': 'n',
    'ó': 'o',
    'ö': 'o',
    'ü': 'u',
    'ú': 'u',
    "’": '',
    '(': '',
    ')': '',
    '[': '',
    ']': '',
    '"': '',
    '-': ' ',
    '~': '',
    'í': 'i'
  }
  return chars_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_linkedin_identifiers_function():
  arr = [
    'she/her/hers',
    'she/her/ella',
    'ella/she',
    'she/her',
    'they/he',
    'he/him',
    '/his',
    '/ela',
    'shrm cp',
    'phd',
    'mba',
    'ccp',
    'shrm',
    'scp',
    'ms',
    'mhr',
    'he/',
    'cdr',
    '/phr'
  ]
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_emails_to_delete_function():
  custom_set = {
    'christopher.pappas@datadoghq.com',
    'keyonne.session@datadoghq.com',
    'megan.hester@datadoghq.com',
    'neha.patel@fanduel.com',
    'mysh.brownell@fanduel.com',
    'mysh.ccp@fanduel.com',
    'alex.desbiens@mongodb.com',
    'alex.thompson@mongodb.com',
    'hgutstein@nextdoor.com',
    'mahmed@nextdoor.com',
    'abastawy@opentable.com',
    'ayoussef@opentable.com',
    'mowens@opentable.com',
    'joseph.ortiz@datadoghq.com',
    'aly.oconnor@datadoghq.com',
    'matthew.matilsky@datadoghq.com',
    'jooryun.jessica@datadoghq.com',
    'jooryun.woo@datadoghq.com',
    'meggan.astarita@hellofresh.com',
    'joseph.albano@hellofresh.com',
    'elyse.alaimo@hellofresh.com',
    'melissa.lalic@hellofresh.com',
    'tabitha.hammond@hellofresh.com',
    'katy.johnson@hellofresh.com',
    'logan.boyko@hellofresh.com',
    'zachary.mccann@hellofresh.com',
    'patrick.ouedraogo@hellofresh.com',
    'caroline.bavaro@hellofresh.com',
    'jake.fox@datadoghq.com',
    'gmoore@nextdoor.com',
    'roneill@nextdoor.com',
    'rhong@nextdoor.com',
    'stynan@nextdoor.com',
    'dcockey@nextdoor.com',
    'gsaca@nextdoor.com',
    'achennagiri@nextdoor.com',
    'amacmannis@nextdoor.com',
    'gdessert@nextdoor.com',
    'ifernandez@nextdoor.com',
    'mkhoa@nextdoor.com',
    'mnguyen@nextdoor.com',
    'jmerjeski@nextdoor.com',
    'erooney@netflix.com',
    'mfranco@netflix.com',
    'gthompson@netflix.com',
    'evolden@netflix.com',
    'smorris@opentable.com',
    'rkargas@opentable.com',
    'syoung@opentable.com',
    'mrhodes@opentable.com',
    'mgreenberg@opentable.com',
    'cstangland@opentable.com',
    'akhumsaard@opentable.com',
    'mlocquiao@opentable.com',
    'bkhalifa@opentable.com',
    'cpopelka@opentable.com',
    'tthoren@opentable.com',
    'sday@opentable.com',
    'bclark@opentable.com',
    'mjo@opentable.com',
    'mspecht@opentable.com',
    'bsnodgrass@opentable.com',
    'ljohannesen@opentable.com',
    'nibrahem@opentable.com',
    'mdavis@opentable.com',
    'aross@opentable.com',
    'gmartin@opentable.com',
    'gproctor@opentable.com',
    'myoussef@opentable.com',
    'skirchmann@opentable.com',
    'korourke@opentable.com',
    'alysse.coe@fanduel.com',
    'samit@nextdoor.com',
    'ssalam@nextdoor.com',
    'afrain@nextdoor.com',
    'ccade@nextdoor.com',
    'rbrogan@nextdoor.com',
    'minji.kim@mongodb.com',
    'madeline.gerlach@mongodb.com',
    'gizem.kocak@mongodb.com',
    'roseann.nairooz@mongodb.com',
    'allison.frain@mongodb.com',
    'alina.arias@mongodb.com',
    'kristian.nunez@mongodb.com',
    'darley.coby@mongodb.com',
    'zachary.starkey@mongodb.com',
    'cassidy.cade@mongodb.com',
    'taijah.harris@mongodb.com',
    'taijah.tucker@mongodb.com',
    'alex.roque@mongodb.com',
    'jackie.lagares@mongodb.com',
    'vic.thadhani@mongodb.com',
    'amurray@netflix.com',
    'msalazar@netflix.com',
    'rmiller@netflix.com',
    'hahmed@opentable.com',
    'debbie.savittieri@hellofresh.com',
    'tracy.demaggio@hellofresh.com',
    'daniel.kim@hellofresh.com',
    'filippa.stewart@hellofresh.com',
    'iwona.kurczab@hellofresh.com',
    'donna.curran@hellofresh.com',
    'lisa.engel@hellofresh.com',
    'angela.lentini@hellofresh.com',
    'andreza.frattini@hellofresh.com',
    'emily.owen@hellofresh.com',
    'kaylee.langbridge@hellofresh.com',
    'darius.lumpkins@hellofresh.com',
    'stephanie.tleiji@hellofresh.com',
    'maximiliano.trujillo@hellofresh.com',
    'maximiliano.diaz@hellofresh.com',
    'shante.mogenet@hellofresh.com',
    'michael.matt@hellofresh.com',
    'ana.sofia@hellofresh.com',
    'ana.silva@hellofresh.com',
    'aylin.senturk@hellofresh.com',
    'bianca.cohn@hellofresh.com',
    'owen.choi@hellofresh.com',
    'natalia.howard@hellofresh.com',
    'meredith.fortney@hellofresh.com',
    'odette.wiggers@hellofresh.com',
    'edwina.perfanov@hellofresh.com',
    'edwina.ritchard@hellofresh.com',
    'marko.marinkovic@hellofresh.com',
    'joanna.mark@hellofresh.com',
    'komal.gopi@hellofresh.com',
    'mary.kate@hellofresh.com',
    'mary.connors@hellofresh.com',
    'david.merriman@hellofresh.com',
    'katie.austerberry@hellofresh.com',
    'marie.sophie@hellofresh.com',
    'marie.gabagnou@hellofresh.com',
    'kaitlin.brooks@datadoghq.com',
    'jordan.blake@datadoghq.com',
    'doireann.oneill@datadoghq.com',
    'kristen.guerrero@datadoghq.com',
    'anthony.andrew@datadoghq.com',
    'anthony.stargill@datadoghq.com',
    'joshua.fang@datadoghq.com',
    'alexandra.rallis@datadoghq.com',
    'annmarie.mellon@datadoghq.com',
    'ryan.scott@datadoghq.com',
    'emily.burke@datadoghq.com',
    'megan.knowles@datadoghq.com',
    'gabriella.victoria@datadoghq.com',
    'jo.rita@datadoghq.com',
    'jo.risola@datadoghq.com',
    'jose.quito@fanduel.com',
    'emily.lee@fanduel.com',
    'gabrielle.ouellette@fanduel.com',
    'emily.king@fanduel.com',
    'danielle.wittpenn@fanduel.com',
    'matthew.bosley@fanduel.com',
    'john.moersdorf@fanduel.com',
    'meghann.walsh@fanduel.com',
    'matthew.etkin@fanduel.com',
    'alvin.tran@fanduel.com',
    'paul.diamond@fanduel.com',
    'alan.karamehmedovic@fanduel.com',
    'christina.coy@fanduel.com',
    'christina.reardon@fanduel.com',
    'alex.yee@fanduel.com',
    'nick.nessel@fanduel.com',
    'taylor.koontz@fanduel.com',
    'scott.patton@fanduel.com',
    'dylan.kessell@fanduel.com',
    'justin.hanke@fanduel.com',
    'chris.burns@fanduel.com',
    'jake.obrien@fanduel.com',
    'lindsay.haupt@fanduel.com',
    'seth.moed@fanduel.com',
    'cait.ford@fanduel.com',
    'alex.otero@fanduel.com',
    'john.prilliman@fanduel.com',
    'erin.henthorn@fanduel.com',
    'kristen.lobosco@fanduel.com',
    'vladimir.loscutoff@fanduel.com',
    'emanuel.adjekum@fanduel.com',
    'allison.bauer@fanduel.com',
    'tianna.shoulars@fanduel.com',
    'aleks.kotlajic@fanduel.com',
    'karim.evelio@fanduel.com',
    'siobhan.mcphillips@fanduel.com',
    'thomas.staton@fanduel.com',
    'kim.bijou@fanduel.com',
    'riley.cannon@fanduel.com',
    'daniel.derrico@fanduel.com',
    'lucy.wemyss@fanduel.com',
    'julio.reynoso@fanduel.com',
    'scott.laine@fanduel.com',
    'jeff.halligan@fanduel.com',
    'steven.morgan@fanduel.com',
    'danielle.hunter@fanduel.com',
    'sejada.mitchell@fanduel.com',
    'jennifer.kaufman@fanduel.com',
    'tricia.alcamo@fanduel.com',
    'brett.arneson@fanduel.com',
    'jason.mezrahi@fanduel.com',
    'ashtine.tapanes@fanduel.com',
    'john.wilkins@fanduel.com',
    'angela.auz@fanduel.com',
    'david.kwon@fanduel.com',
    'david.yi@fanduel.com',
    'sheri.rossinsky@fanduel.com',
    'katie.van@fanduel.com',
    'katie.pelt@fanduel.com',
    'mia.raffa@fanduel.com',
    'blake.velcoff@fanduel.com',
    'blake.gettlin@fanduel.com',
    'keymoni.scott@fanduel.com',
    'keymoni.terry@fanduel.com',
    'joshua.avila@mongodb.com',
    'josh.schwartz@mongodb.com',
    'frances.mckinnely@mongodb.com',
    'pearlina.chhaysymeexo@mongodb.com',
    'justin.embler@mongodb.com',
    'jose.nieto@mongodb.com',
    'karla.otis@mongodb.com',
    'gina.dinello@mongodb.com',
    'meghan.anthony@mongodb.com',
    'jillian.mcsweegan@mongodb.com',
    'brett.ouellette@mongodb.com',
    'elizabeth.mendoza@mongodb.com',
    'kelly.desrosier@mongodb.com',
    'katie.hess@mongodb.com',
    's.amit@mongodb.com',
    's.salam@mongodb.com',
    'tyler.buckley@mongodb.com',
    'callie.furnas@mongodb.com',
    'dayna.chu@mongodb.com',
    'kayla.vespia@mongodb.com',
    'rika.shinozaki@mongodb.com',
    'justin.delman@mongodb.com',
    'frank.lofaro@mongodb.com',
    'cheryl.cove@mongodb.com',
    'jason.zerega@mongodb.com',
    'heather.salazar@mongodb.com',
    'kaitlin.blackmer@mongodb.com',
    'jazmyne.cohen@mongodb.com',
    'jackson.yniguez@mongodb.com',
    'michael.friel@mongodb.com',
    'rockman.ha@mongodb.com',
    'jason.klein@mongodb.com',
    'michael.maccariello@mongodb.com',
    'john.talarico@mongodb.com',
    'chaim.solomon@mongodb.com',
    'hannah.carroll@mongodb.com',
    'mary.gordon@mongodb.com',
    'mary.utt@mongodb.com',
    'patricia.benevent@mongodb.com',
    'danielle.zielinski@mongodb.com',
    'yash.sisodiya@mongodb.com',
    'henasia.wilson@mongodb.com',
    'annie.gull@mongodb.com',
    'courtney.fahrun@mongodb.com',
    'michael.cipriano@mongodb.com',
    'kenny.huggins@mongodb.com',
    'rosaria.velardo@mongodb.com',
    'taryn.ackerman@mongodb.com',
    'joseph.dieguez@mongodb.com',
    'amanda.cuttler@mongodb.com',
    'miraque.hicks@mongodb.com',
    'rohit.rajpoot@mongodb.com',
    'brett.larson@mongodb.com',
    'matthew.baker@mongodb.com',
    'yamini.nigudkar@mongodb.com',
    'georgie.maudslay@mongodb.com',
    'erica.chargar@mongodb.com',
    'freddy.abdilmasih@mongodb.com',
    'khristopher.ahmad@mongodb.com',
    'khristopher.patrick@mongodb.com',
    'haley.ogrady@mongodb.com',
    'matthew.sestokas@mongodb.com',
    'devon.holman@mongodb.com',
    'john.grimm@mongodb.com',
    'kathy.ryan@mongodb.com',
    'robert.zielinski@mongodb.com',
    'mohammed.ahmed@mongodb.com',
    'niyati.shah@mongodb.com',
    'shaun.oshea@mongodb.com',
    'arvind.kumar@mongodb.com',
    'rick.hertel@mongodb.com',
    'khalid.iqbal@mongodb.com',
    'jason.buss@mongodb.com',
    'kimberly.baldeo@mongodb.com',
    'kate.wright@mongodb.com',
    'halley.mccormack@mongodb.com',
    'abi.klein@mongodb.com',
    'arpita.adhikari@mongodb.com',
    'alistair.blake@mongodb.com',
    'dana.teplitsky@mongodb.com',
    'jholsworth@netflix.com',
    'slee@netflix.com',
    'aarias@netflix.com',
    'pclayborn@netflix.com',
    'atreat@netflix.com',
    'amartin@netflix.com',
    'awalsh@netflix.com',
    'cjoy@netflix.com',
    'cperez@netflix.com',
    'klesperance@netflix.com',
    'vnguyen@netflix.com',
    'amiranda@netflix.com',
    'anakamura@netflix.com',
    'chilton@netflix.com',
    'jletizia@netflix.com',
    'rpalmer@netflix.com',
    'mbenigno@netflix.com',
    'cperalta@netflix.com',
    'nyoung@netflix.com',
    'jshih@netflix.com',
    'aschuppe@netflix.com',
    'knguyen@netflix.com',
    'wwong@netflix.com',
    'ktaylor@netflix.com',
    'ajebrock@netflix.com',
    'alim@netflix.com',
    'jgrayson@netflix.com',
    'gnoa@netflix.com',
    'mpryor@netflix.com',
    'jgonzalez@netflix.com',
    'kpatterson@netflix.com',
    'ksleger@netflix.com',
    'mcalderon@netflix.com',
    'pleaf@netflix.com',
    'jhsu@netflix.com',
    'lwamai@netflix.com',
    'jrobinson@netflix.com',
    'skapoor@netflix.com',
    'abader@netflix.com',
    'breynolds@netflix.com',
    'jestipona@netflix.com',
    'mmartinez@netflix.com',
    'ahussain@netflix.com',
    'clopez@netflix.com',
    'mgleaton@netflix.com',
    'bjackson@netflix.com',
    'sdonohue@netflix.com',
    'lfrank@netflix.com',
    'lbatista@netflix.com',
    'jdillon@netflix.com',
    'jlong@netflix.com',
    'sabbondanza@netflix.com',
    'svierra@netflix.com',
    'sbeardsley@netflix.com',
    'arivera@netflix.com',
    'jramirez@netflix.com',
    'jeyzaguirre@netflix.com',
    'keddy@netflix.com',
    'gleung@nextdoor.com',
    'mcave@nextdoor.com',
    'auher@nextdoor.com',
    'kotis@nextdoor.com',
    'bouellette@nextdoor.com',
    'mkim@nextdoor.com',
    'bpower@nextdoor.com',
    'ssong@nextdoor.com',
    'khess@nextdoor.com',
    'pmeawad@nextdoor.com',
    'aarias@nextdoor.com',
    'kvespia@nextdoor.com',
    'flofaro@nextdoor.com',
    'ecoplin@nextdoor.com',
    'fmckinnely@nextdoor.com',
    'pchhaysymeexo@nextdoor.com',
    'jnieto@nextdoor.com',
    'emendoza@nextdoor.com',
    'jembler@nextdoor.com',
    'afederowicz@nextdoor.com',
    'kdesrosier@nextdoor.com',
    'aneff@nextdoor.com',
    'rnairooz@nextdoor.com',
    'tbuckley@nextdoor.com',
    'mgerlach@nextdoor.com',
    'cfurnas@nextdoor.com',
    'dchu@nextdoor.com',
    'dcoby@nextdoor.com',
    'fcamara@nextdoor.com',
    'hmyers@nextdoor.com',
    'mdrizen@nextdoor.com',
    'tharris@nextdoor.com',
    'ttucker@nextdoor.com',
    'ccove@nextdoor.com',
    'knunez@nextdoor.com',
    'rshinozaki@nextdoor.com',
    'gdinello@nextdoor.com',
    'zstarkey@nextdoor.com',
    'kzinchiak@nextdoor.com',
    'hsalazar@nextdoor.com',
    'csolomon@nextdoor.com',
    'pbenevent@nextdoor.com',
    'jmcsweegan@nextdoor.com',
    'hwilson@nextdoor.com',
    'mgordon@nextdoor.com',
    'mutt@nextdoor.com',
    'cfahrun@nextdoor.com',
    'hbrenner@nextdoor.com',
    'agull@nextdoor.com',
    'msestokas@nextdoor.com',
    'tackerman@nextdoor.com',
    'rzielinski@nextdoor.com',
    'hogrady@nextdoor.com',
    'acuttler@nextdoor.com',
    'kryan@nextdoor.com',
    'jdelman@nextdoor.com',
    'greynoso@nextdoor.com',
    'marmstrong@nextdoor.com',
    'jtalarico@nextdoor.com',
    'kblackmer@nextdoor.com',
    'ysisodiya@nextdoor.com',
    'dzielinski@nextdoor.com',
    'cmellett@nextdoor.com',
    'hcarroll@nextdoor.com',
    'jgrimm@nextdoor.com',
    'khuggins@nextdoor.com',
    'mcipriano@nextdoor.com',
    'jvenditti@nextdoor.com',
    'rvelardo@nextdoor.com',
    'dholman@nextdoor.com',
    'jdieguez@nextdoor.com',
    'manthony@nextdoor.com',
    'mlocquiao@nextdoor.com',
    'atre@nextdoor.com',
    'atrevino@nextdoor.com',
    'smoore@nextdoor.com',
    'afarahmand@nextdoor.com',
    'sayubi@nextdoor.com',
    'vdominguez@nextdoor.com',
    'dmonahan@nextdoor.com',
    'rlin@nextdoor.com',
    'asingh@nextdoor.com',
    'ckobe@nextdoor.com',
    'tdavis@nextdoor.com',
    'cneafsey@nextdoor.com',
    'tbara@nextdoor.com',
    'ajew@nextdoor.com',
    'snummi@nextdoor.com',
    'cedwards@nextdoor.com',
    'mcrescenzo@nextdoor.com',
    'korourke@nextdoor.com',
    'sabdulkabir@nextdoor.com',
    'ajohnson@nextdoor.com',
    'agorelick@nextdoor.com',
    'awright@nextdoor.com',
    'amacedo@nextdoor.com',
    'jkaynatma@nextdoor.com',
    'jlloyd@nextdoor.com',
    'jroberts@nextdoor.com',
    'lcandelaria@nextdoor.com',
    'ltyler@nextdoor.com',
    'eekong@nextdoor.com',
    'dfreund@nextdoor.com',
    'lbusse@nextdoor.com',
    'lgeagan@nextdoor.com',
    'cheimbuch@nextdoor.com',
    'abathke@nextdoor.com',
    'rgerke@nextdoor.com',
    'dkilponen@nextdoor.com',
    'ckoski@nextdoor.com',
    'smengistu@opentable.com',
    'sghai@opentable.com',
    'sross@opentable.com',
    'aabdelrazek@opentable.com',
    'kortiz@opentable.com',
    'nmosaad@opentable.com',
    'nshah@opentable.com',
    'scurtis@opentable.com',
    'kperkins@opentable.com',
    'ssaelee@opentable.com',
    'jmohamed@opentable.com',
    'ckobe@opentable.com',
    'nszathmary@opentable.com',
    'aborhan@opentable.com',
    'cray@opentable.com',
    'mmathewson@opentable.com',
    'sgonzales@opentable.com',
    'eswan@opentable.com',
    'eguite@opentable.com',
    'ajarvis@opentable.com',
    'stawfeek@opentable.com',
    'kebeido@opentable.com',
    'aali@opentable.com',
    'mhutchinson@opentable.com',
    'dsaber@opentable.com',
    'yelsayed@opentable.com',
    'lwang@opentable.com',
    'rsakr@opentable.com',
    'aatef@opentable.com',
    'jmccormick@opentable.com',
    'jsampson@opentable.com',
    'clamb@opentable.com',
    'sko@opentable.com',
    'cassandra.colangelo@salesforce.com',
    'megan.barcevac@salesforce.com',
    'lauren.buhrow@salesforce.com',
    'john.mcginnes@salesforce.com',
    'jason.alcorn@salesforce.com',
    'shamel.bratton@salesforce.com',
    'gina.johnson@salesforce.com',
    'jessica.schmidt@salesforce.com',
    'timothy.kerwin@salesforce.com',
    'jenny.pigott@salesforce.com',
    'brittany.totino@salesforce.com',
    'karla.otis@salesforce.com',
    'kelly.desrosier@salesforce.com',
    'katie.hess@salesforce.com',
    'christopher.marte@salesforce.com',
    'kayla.vespia@salesforce.com',
    'rika.shinozaki@salesforce.com',
    'cheryl.cove@salesforce.com',
    'joseph.dieguez@salesforce.com',
    'haley.ogrady@salesforce.com',
    'elena.belova@salesforce.com',
    'ritu.patel@salesforce.com',
    'kristina.levinton@salesforce.com',
    'grace.freyre@salesforce.com',
    'vincent.dinh@salesforce.com',
    'victoria.firestone@salesforce.com',
    'victoria.conway@salesforce.com',
    'kevin.fanning@salesforce.com',
    'chad.siemens@salesforce.com',
    'cassidy.cade@salesforce.com',
    'rob.gifford@salesforce.com',
    'marissa.maitner@salesforce.com',
    'elizabeth.mendoza@salesforce.com',
    'anant.dhaka@salesforce.com',
    'callie.furnas@salesforce.com',
    'alina.arias@salesforce.com',
    'olivia.fox@salesforce.com',
    'brai.beckel@salesforce.com',
    'stacey.berger@salesforce.com',
    'nicole.sway@salesforce.com',
    'william.ramgadoo@salesforce.com',
    'lb.hernandez@salesforce.com',
    'jackson.yniguez@salesforce.com',
    'michael.nocco@salesforce.com',
    'manal.guennad@salesforce.com',
    'alex.desbiens@salesforce.com',
    'alex.thompson@salesforce.com',
    'elizabeth.caccia@salesforce.com',
    'elizabeth.kelly@salesforce.com',
    'matthew.baker@salesforce.com',
    'jade.hodge@salesforce.com',
    'teryn.terrazas@salesforce.com',
    'zachary.terracciano@salesforce.com',
    'rifton.westby@salesforce.com',
    'samantha.turk@salesforce.com',
    'vani.varma@salesforce.com',
    'raven.ellis@salesforce.com',
    'susan.weiss@salesforce.com',
    'hinal.patel@salesforce.com',
    'narmadha.ediga@salesforce.com',
    'max.becker@salesforce.com',
    'elizabeth.grein@salesforce.com',
    'nick.ronzino@salesforce.com',
    'terrence.obrien@salesforce.com',
    'sarah.sekulovic@salesforce.com',
    'lisa.muoio@salesforce.com',
    'lisa.accardi@salesforce.com',
    'ashley.nelson@salesforce.com',
    'ashley.parker@salesforce.com',
    'kat.unfried@salesforce.com',
    'catherine.tran@salesforce.com',
    'ethan.mao@salesforce.com',
    'wes.francisco@salesforce.com',
    'jose.chamorro@salesforce.com',
    'brian.lloyd@salesforce.com',
    'zinzi.blackbeard@salesforce.com',
    'nikita.desai@salesforce.com',
    'victoria.lourenco@salesforce.com',
    'suezette.yasmin@salesforce.com',
    'joseph.smyth@salesforce.com',
    'kelly.lezynski@salesforce.com',
    'alexandra.kahen@salesforce.com',
    'ellen.schier@salesforce.com',
    'kelsey.kotlarek@salesforce.com',
    'katie.leasure@salesforce.com',
    'chandler.basconcillo@salesforce.com',
    'cherish.shinholster@salesforce.com',
    'bridie.ledwell@salesforce.com',
    'shana.hoey@salesforce.com',
    'lindsey.bruns@salesforce.com',
    'kamalika.bhattacharya@salesforce.com',
    'manjari.saxena@salesforce.com',
    'jeff.vadukumcherry@salesforce.com',
    'shauna.kauth@salesforce.com',
    'michele.stewart@salesforce.com',
    'gabriela.silva@salesforce.com',
    'ashley.morris@salesforce.com',
    'gillian.kern@salesforce.com',
    'suzie.steenberge@salesforce.com',
    'jacqueline.hicks@salesforce.com',
    'jessica.garcia@salesforce.com',
    'rajnish.jindal@salesforce.com',
    'jessica.lupo@salesforce.com',
    'michelle.huang@salesforce.com',
    'robert.porter@salesforce.com',
    'rajeshwar.kumar@salesforce.com',
    'rajeshwar.bomma@salesforce.com',
    'james.hairston@salesforce.com',
    'david.hoggan@salesforce.com',
    'grace.bibby@salesforce.com',
    'junu.phillips@salesforce.com',
    'alicia.schriever@salesforce.com',
    'michelle.mccarthy@salesforce.com',
    'jill.donnelly@salesforce.com',
    'andrea.hurni@salesforce.com',
    'andrea.rigoglioso@salesforce.com',
    'randy.kishun@salesforce.com',
    'fernando.tenesaca@salesforce.com',
    'nicole.pryt@salesforce.com',
    'zac.demarco@salesforce.com',
    'marcos.palacios@salesforce.com',
    'caitlin.bourn@salesforce.com',
    'laura.golubic@salesforce.com',
    'ariadna.diaz@salesforce.com',
    'pete.kim@loreal.com',
    'nadia.mathews@loreal.com',
    'wendy.liem@loreal.com',
    'zahava.goldfischer@loreal.com',
    'kathy.ryan@loreal.com',
    'christina.necci@loreal.com',
    'kelly.desrosier@loreal.com',
    'ratika.rajpal@loreal.com',
    'cheryl.cove@loreal.com',
    'kaitlin.blackmer@loreal.com',
    'michele.sullivan@loreal.com',
    'faye.alba@loreal.com',
    'loreal.simpson@loreal.com',
    'michael.wehbé@loreal.com',
    'michael.wehbe@loreal.com',
    'christopher.marte@loreal.com',
    'rika.shinozaki@loreal.com',
    'geraldine.zenteno@loreal.com',
    'john.talarico@loreal.com',
    'ashley.lamberti@loreal.com',
    'alina.arias@loreal.com',
    'verónica.bulka@loreal.com',
    'olivia.fox@loreal.com',
    'jackie.lagares@loreal.com',
    'melanie.hunter@loreal.com',
    'lida.chaplynsky@loreal.com',
    'karla.otis@loreal.com',
    'geraldine.mariela@loreal.com',
    'geraldine.garnica@loreal.com',
    'matt.sundel@loreal.com',
    'ashley.pilesky@loreal.com',
    'charlotte.gagnier@loreal.com',
    'verónica.castillo@loreal.com',
    'isabelle.thériault@loreal.com',
    'nicolas.sar@loreal.com',
    'wendy.reyes@loreal.com',
    'marilyn.eber@loreal.com',
    'michael.wehbe@loreal.com',
    'yfarfan@figma.com',
    'pmangione@figma.com',
    'calfieri@figma.com',
    'kjordan@figma.com',
    'avyas@figma.com',
    'jyoo@figma.com',
    'jacob.gassett@mybrightwheel.com',
    'amanda.conley@mybrightwheel.com',
    'audrey.kosydor@mybrightwheel.com',
    'connor.cannon@mybrightwheel.com',
    'mara.green@mybrightwheel.com',
    'samantha.zeller@mybrightwheel.com',
    'lisa.rothhaar@mybrightwheel.com',
    'anari.ormond@mybrightwheel.com',
    'jacob.paul@mybrightwheel.com',
    'sabrina.silva@mybrightwheel.com',
    'victoria.alonso@mybrightwheel.com',
    'amir.hakimjavadi@mybrightwheel.com',
    'kyle.roy@mybrightwheel.com',
    'larissa.howlett@mybrightwheel.com',
    'joelle.lowe@mybrightwheel.com',
    'kerry.aldrich@mybrightwheel.com',
    'raymond.miller@mybrightwheel.com',
    'kat.kelley@mybrightwheel.com',
    'sarah.byron@mybrightwheel.com',
    'amanda.brown@mybrightwheel.com',
    'sarah.dye@mybrightwheel.com',
    'claudia.wallace@mybrightwheel.com',
    'madeline.haimes@mybrightwheel.com',
    'annie.ciacchini@mybrightwheel.com',
    'sabrina.poblete@mybrightwheel.com',
    'julia.spector@mybrightwheel.com',
    'lily.finkle@mybrightwheel.com',
    'samantha.martin@mybrightwheel.com',
    'sarah.durst@mybrightwheel.com',
    'daniel.shapero@mybrightwheel.com',
    'travon.brooks@mybrightwheel.com',
    'jaime.tavarez@mybrightwheel.com',
    'chloe.scheer@mybrightwheel.com',
    'ryan.chance@mybrightwheel.com',
    'joshua.carrasquillo@mybrightwheel.com',
    'christian.pena@mybrightwheel.com',
    'amy.crifasi@mybrightwheel.com',
    'donalee.jones@mybrightwheel.com',
    'maia.josebachvili@mybrightwheel.com',
    'megan.fleming@mybrightwheel.com',
    'mhardy@atlassian.com',
    'umajithia@atlassian.com',
    'mcullen@atlassian.com',
    'evan@atlassian.com',
    'emiles@atlassian.com',
    'pchung@atlassian.com',
    'uraithatha@atlassian.com',
    'earsdell@atlassian.com',
    'shanley@atlassian.com',
    'khoedt@atlassian.com',
    'aliu@atlassian.com',
    'shalligan@atlassian.com',
    'tlohar@atlassian.com',
    'mrivera@atlassian.com',
    'jsaunders@atlassian.com',
    'vtsang@atlassian.com',
    'zdumke@atlassian.com',
    'mellen@atlassian.com',
    'jpetty@atlassian.com',
    'klester@atlassian.com',
    'kwoods@atlassian.com',
    'ktaylor@atlassian.com',
    'nicole.sarillo@hinge.co',
    'david.konstantinov@hinge.co',
    'amanda.godburn@hinge.co',
    'alberto.gorini@hinge.co',
    'tyler.wong@hinge.co',
    'ian.sautner@hinge.co',
    'alice.jorgenson@hinge.co',
    'david.dk@hinge.co',
    'katy.lowry@hinge.co',
    'kayleigh.crow@hinge.co',
    'traci.barone@hinge.co',
    'noele.kaykas@hinge.co',
    'tara.hurley@hinge.co',
    'ivy.rivero@hinge.co',
    'joan.sramek@hinge.co',
    'kelvin.chu@hinge.co',
    'randy.lam@hinge.co',
    'brian.montgomery@hinge.co',
    'suraj.mahato@hinge.co',
    'jillian.hanna@hinge.co',
    'jessica.winkle@hinge.co',
    'trey.oubre@hinge.co',
    'alaina.schnipke@hinge.co',
    'zachary.livingston@hinge.co',
    'michelle.lamoureux@hinge.co',
    'mariah.bowser@hinge.co',
    'elle.estares@hinge.co',
    'carrie.poulos@hinge.co',
    'lauren.runte@hinge.co',
    'rachel.white@hinge.co',
    'miraque.hicks@hinge.co',
    'madeleine.clelland@hinge.co',
    'michelle.diaz@hinge.co',
    'michelle.estrin@hinge.co',
    'jamel.exhem@hinge.co',
    'elisa.scott@hinge.co',
    'saurabh.shah@hinge.co',
    'troy.barba@hinge.co',
    'brianna.chavez@hinge.co',
    'kevin.wong@hinge.co',
    'vincent.shea@hinge.co',
    'michelle.williams@hinge.co',
    'lyndsey.bentley@hinge.co',
    'elle.michelle@hinge.co',
    'jim.divita@hinge.co',
    'guillaume.dorado@hinge.co',
    'lauren.mcdermott@hinge.co',
    'brandon.woods@hinge.co',
    'ed.zhang@hinge.co',
    'scarter@grubhub.com',
    'mmaddox@grubhub.com',
    'apatel@grubhub.com',
    'sbuechnert@grubhub.com',
    'scipriano@grubhub.com',
    'mdamico@grubhub.com',
    'hmadera@grubhub.com',
    'mlissa@grubhub.com',
    'nvlasic@grubhub.com',
    'eliz@grubhub.com',
    'cstewart@grubhub.com',
    'kcsaszar@grubhub.com',
    'sbhathal@grubhub.com',
    'mbakula@grubhub.com',
    'srydberg@grubhub.com',
    'hartiles@grubhub.com',
    'ajohnston@grubhub.com',
    'gdanino@grubhub.com',
    'kstec@grubhub.com',
    'elafferty@grubhub.com',
    'ishulman@grubhub.com',
    'kstovall@grubhub.com'
    'kim.thuy@tinder.com',
    'sammy.johnson@tinder.com',
    'chanell.jones@tinder.com',
    'nora.diaz@tinder.com',
    'guillaume.dorado@tinder.com',
    'andy.cdr@tinder.com',
    'brian.haney@tinder.com',
    'ashley.wang@tinder.com',
    'nora.deleon@tinder.com',
    'nicole.sidaros@capitalone.com',
    'vijay.pant@capitalone.com',
    'cassandra.nunez@capitalone.com',
    'pliberski@lyft.com',
    'iayyeh@lyft.com',
    'bperez@lyft.com',
    'rsarayba@lyft.com',
    'drose@lyft.com',
    'kohri@lyft.com',
    'ksharma@lyft.com',
    'mcouper@lyft.com',
    'nsarsour@lyft.com',
    'rpotter@lyft.com',
    'donejeme@lyft.com',
    'zmatthews@lyft.com',
    'thouser@lyft.com',
    'mwong@lyft.com',
    'gstockwell@lyft.com',
    'mfernanda@lyft.com',
    'mrice@lyft.com',
    'mochoa@lyft.com',
    'tbrunsdale@lyft.com',
    'apetrova@lyft.com',
    'jhernandez@lyft.com',
    'marissa.passick@grammarly.com',
    'emeier@pinterest.com',
    'mparis@pinterest.com',
    'skaiser@pinterest.com',
    'blyn@pinterest.com',
    'bryan@pinterest.com',
    'ktran@pinterest.com',
    'jharris@pinterest.com',
    'mmasata@pinterest.com',
    'ehandley@pinterest.com',
    'pwilliams@pinterest.com',
    'lgarcia@pinterest.com',
    'abalivet@pinterest.com',
    'ewashington@pinterest.com',
    'acrutison@pinterest.com',
    'krobinson@pinterest.com',
    'lesliewainscott@upwork.com',
    'lesliescp@upwork.com',
    'megandias@upwork.com',
    'vincentvallador@upwork.com',
    'saramarieshine@upwork.com',
    'naveedahmad@upwork.com',
    'ramyaram@upwork.com',
    'umaizashah@upwork.com',
    'michaelfernandez@upwork.com',
    'princepalkaur@upwork.com',
    'oghenetegavuevu@upwork.com',
    'justinlee@upwork.com',
    'adamsablay@upwork.com',
    'mimioconnell@upwork.com',
    'jesirietuazon@upwork.com',
    'bengahlsdorf@upwork.com',
    'jesmonidrisslachance@upwork.com',
    'elizabethhelfert@upwork.com',
    'kellywambui@upwork.com',
    'axselrose@upwork.com',
    'stephaniecloutier@upwork.com',
    'daniellemimoni@upwork.com',
    'joycelynscott@upwork.com',
    'marlierosario@upwork.com',
    'anuragchauhan@upwork.com',
    'lesliecotton@upwork.com',
    'leslieshrm@upwork.com',
    'meganelizabeth@upwork.com',
    'vincentpaul@upwork.com',
    'vasudev@upwork.com',
    'mimigreen@upwork.com',
    'mariamkereselidze@upwork.com',
    'jessicabelle@upwork.com',
    'klaragizova@upwork.com',
    'kellykoigi@upwork.com',
    'carolinahanysz@upwork.com',
    'axselmaprangala@upwork.com',
    'waelabdelmonem@upwork.com',
    'joycelynhunter@upwork.com',
    'marliedel@upwork.com',
    'karentoledo@upwork.com',
    'jp.pawlikowski@circle.com',
    'yu.riley@circle.com',
    'tim.wing@circle.com',
    'spencer.crane@circle.com',
    'meghan.giraud@circle.com',
    'yu.chang@circle.com',
    'sydney.leffler@circle.com',
    'benjamin.andersen@circle.com',
    'yu.chen@circle.com',
    'acorral@forhims.com',
    'ncecchini@forhims.com',
    'knovak@forhims.com',
    'kda@forhims.com',
    'ksilva@forhims.com',
    'jslack@forhims.com',
    'tmensah@forhims.com',
    'nkeith@forhims.com',
    'pam@nuna.com',
    'nuna@nuna.com',
    'connie@nuna.com',
    'ramona@nuna.com',
    'lucky@nuna.com',
    'romina@nuna.com',
    'francesca@nuna.com',
    'nesrin@nuna.com',
    'cassidy@nuna.com',
    'federica@nuna.com',
    'fern@nuna.com',
    'nicole@nuna.com',
    'lia@nuna.com',
    'shir@nuna.com',
    'triana@nuna.com',
    'fran@nuna.com',
    'dianne@nuna.com',
    'bev@nuna.com',
    'christopher@nuna.com',
    'liza@nuna.com',
    'rikki@nuna.com',
    'cherise@nuna.com',
    'dpopolo@cloudflare.com',
    'irodrigues@cloudflare.com',
    'apappathi@cloudflare.com',
    'hduan@cloudflare.com',
    'ijoao@cloudflare.com',
    'mlewis@cloudflare.com',
    'bkander@cloudflare.com',
    'kwinkler@cloudflare.com',
    'rpais@cloudflare.com',
    'tbi@cloudflare.com',
    'yyue@cloudflare.com',
    'mmckamey@cloudflare.com',
    'cflagler@cloudflare.com',
    'gchan@cloudflare.com',
    'mmullins@cloudflare.com',
    'wnodine@cloudflare.com',
    'ksopko@cloudflare.com',
    'jnguyen@cloudflare.com',
    'aarut@cloudflare.com',
    'ajeevagan@cloudflare.com',
    'vbayfield@cloudflare.com',
    'slee@cloudflare.com',
    'tderadourian@cloudflare.com',
    'cconnors@cloudflare.com',
    'rserraj@cloudflare.com',
    'gblackmon@cloudflare.com',
    'szdarko@cloudflare.com',
    'ddeams@cloudflare.com',
    'cpurvis@cloudflare.com',
    'cpatel@deloitte.com',
    'nshmuely@deloitte.com',
    'amarchesi@deloitte.com',
    'smiskura@deloitte.com',
    'llazear@deloitte.com',
    'lcristescu@deloitte.com',
    'lms@deloitte.com',
    'jjiganti@deloitte.com',
    'sevans@deloitte.com',
    'samaraweera@deloitte.com',
    'mgaeta@deloitte.com',
    'msallis@deloitte.com',
    'jjenkins@deloitte.com',
    'klarkin@deloitte.com',
    'bdavis@deloitte.com',
    'ldesiderio@deloitte.com',
    'lnatalie@deloitte.com',
    'jdelahoyd@deloitte.com',
    'vli@deloitte.com',
    'jbanks@deloitte.com',
    'kvance@deloitte.com',
    'klaporte@deloitte.com',
    'ekang@deloitte.com',
    'ebarron@deloitte.com',
    'mjain@deloitte.com',
    'cmorgan@deloitte.com',
    'bgardner@deloitte.com',
    'alana.obrien@zoominfo.com',
    'kyle.ada@zoominfo.com',
    'aylee.bourbon@zoominfo.com',
    'drew.smith@zoominfo.com',
    'samuel.machonis@zoominfo.com',
    'kaytelynd.kelley@zoominfo.com',
    'tyler.pobursky@zoominfo.com',
    'joe.prespolis@zoominfo.com',
    'karen.casey@zoominfo.com',
    'sarthak.garg@zoominfo.com',
    'amathur@ancestry.com',
    'myavrom@ancestry.com',
    'klittle@ancestry.com',
    'hgordon@ancestry.com',
    'mmiffy@ancestry.com',
    'achatwin@ancestry.com',
    'mtani@ancestry.com',
    'ble@ancestry.com',
    'mdeok@ancestry.com',
    'sraines@ancestry.com',
    'mharris@ancestry.com',
    'jesplin@ancestry.com',
    'ilana.malul@siriusxm.com',
    'jaimie.hickey@siriusxm.com',
    'shelley.wooten@siriusxm.com',
    'alexandra.allie@siriusxm.com',
    'adam.feldman@siriusxm.com',
    'carl.dangio@siriusxm.com',
    'brendan.cronin@siriusxm.com',
    'ilana.mizrahi@siriusxm.com',
    'kim.cunningham@siriusxm.com',
    'rylee.soule@siriusxm.com',
    'rylee.nicodemus@siriusxm.com',
    'ashlie.yaeger@siriusxm.com',
    'stephanie.saggese@siriusxm.com',
    'karen.batcheller@siriusxm.com',
    'morgan.james@siriusxm.com',
    'leah.shaver@siriusxm.com',
    'trenton.hughes@siriusxm.com',
    'jason.mezrahi@siriusxm.com',
    'elizabeth.rosato@siriusxm.com',
    'elizabeth.moore@siriusxm.com',
    'amber.gomez@doordash.com',
    'annie.whitford@doordash.com',
    'mike.desanto@doordash.com',
    'tina.wolford@doordash.com',
    'alyssa.sacco@doordash.com',
    'bekah.rodriguez@doordash.com',
    'ella.johnstone@doordash.com',
    'marc.scoran@doordash.com',
    'james.kunna@doordash.com',
    'kathy.coughlin@doordash.com',
    'kimberly.sentachi@doordash.com',
    'jenna.tulman@doordash.com',
    'michelle.hasty@doordash.com',
    'rachel.matos@doordash.com',
    'rachel.meyer@doordash.com',
    'taleen.shekerjian@doordash.com',
    'gregorio.labrado@doordash.com',
    'olivia.vandervoort@doordash.com',
    'steph.vaye@doordash.com',
    'dominique.lindsey@doordash.com',
    'kathy.ortiz@doordash.com',
    'yvette.martinez@doordash.com',
    'zachary.davis@doordash.com',
    'bhupinder.singh@doordash.com',
    'jessica.morales@doordash.com',
    'joe.villa@doordash.com',
    'christopher.prasad@doordash.com',
    'sagar.patel@doordash.com',
    'cailen@retool.com',
    'marissa@retool.com',
    'gabriel@retool.com',
    'fung@retool.com',
    'justin@retool.com',
    'colton.zirkle@mongodb.com',
    'emily.oconnell@mongodb.com',
    'hannah.grossfield@mongodb.com',
    'ankur.lion@mongodb.com',
    'alex.bissell@mongodb.com',
    'silvia.jimenez@mongodb.com',
    'caitlyn.kupski@mongodb.com',
    'em.blankenberger@mongodb.com',
    'debbie.proctor@mongodb.com',
    'steven.troup@mongodb.com',
    'pavi.vetriselvan@mongodb.com',
    'aniruddh.deshmukh@mongodb.com',
    'lauren.lootein@artera.io',
    'ryani@zillowgroup.com',
    'stephaniem@zillowgroup.com',
    'erick@zillowgroup.com',
    'tiffanyh@zillowgroup.com',
    'nakiesham@zillowgroup.com',
    'andreas@zillowgroup.com',
    'nicolej@zillowgroup.com',
    'victoriac@zillowgroup.com',
    'jaydew@zillowgroup.com',
    'fabienneg@zillowgroup.com',
    'josephc@zillowgroup.com',
    'nikm@zillowgroup.com',
    'danielm@zillowgroup.com',
    'josephf@zillowgroup.com',
    'acardiob@zillowgroup.com',
    'jordanf@zillowgroup.com',
    'eleonoran@zillowgroup.com',
    'calliem@zillowgroup.com',
    'kellyw@zillowgroup.com',
    'aparajitap@zillowgroup.com',
    'mcc@zillowgroup.com',
    'benjaminf@zillowgroup.com',
    'rozh@zillowgroup.com',
    'katiee@zillowgroup.com',
    'jonathans@zillowgroup.com',
    'jonathank@zillowgroup.com',
    'davidg@zillowgroup.com',
    'michaelr@zillowgroup.com',
    'tima@zillowgroup.com',
    'lisam@zillowgroup.com',
    'wendyj@zillowgroup.com',
    'moniqued@zillowgroup.com',
    'connoro@zillowgroup.com',
    'jayt@zillowgroup.com',
    'jasonc@zillowgroup.com',
    'chrisb@zillowgroup.com',
    'amirc@zillowgroup.com',
    'aparajitaa@zillowgroup.com',
    'ashleyl@zillowgroup.com',
    'janes@zillowgroup.com',
    'jonathanf@zillowgroup.com',
    'andyp@zillowgroup.com',
    'abbassh@zillowgroup.com',
    'joet@zillowgroup.com',
    'kamekol@zillowgroup.com',
    'fernandom@zillowgroup.com',
    'kevinh@zillowgroup.com',
    'jayder@zillowgroup.com',
    'fabiennel@zillowgroup.com',
    'osagiea@zillowgroup.com',
    'toris@zillowgroup.com',
    'makedac@zillowgroup.com',
    'paigec@zillowgroup.com',
    'rachell@zillowgroup.com',
    'reneef@zillowgroup.com',
    'seanb@zillowgroup.com',
    'courtneyc@zillowgroup.com',
    'stephaniet@zillowgroup.com',
    'kenr@zillowgroup.com',
    'stevem@zillowgroup.com',
    'peterb@zillowgroup.com',
    'sarahm@zillowgroup.com',
    'wendys@zillowgroup.com',
    'clyn@nextdoor.com',
    'aamor@nextdoor.com',
    'hguan@nextdoor.com',
    'slatorre@nextdoor.com',
    'cpcc@nextdoor.com',
    'handersen@nextdoor.com',
    'mmell@nextdoor.com',
    'adaniels@nextdoor.com',
    'kburke@nextdoor.com',
    'mbosch@nextdoor.com',
    'sfernando@nextdoor.com',
    'sudaltsova@nextdoor.com',
    'amy.roettger@aexp.com',
    'valentina.scotto@aexp.com',
    'valentina.carlo@aexp.com',
    'maria.keen@aexp.com',
    'alisha.hira@aexp.com',
    'alan.esparza@aexp.com',
    'shobana.jeyaraj@aexp.com',
    'taylor.luu@aexp.com',
    'bridgette.mason@aexp.com',
    'valentina.di@aexp.com',
    'anas.choudhary@aexp.com',
    'paola.nunez@aexp.com',
    'dana.hertz@aexp.com',
    'linda.nsufor@aexp.com',
    'marrissa.jones@aexp.com',
    'jia.wen@aexp.com',
    'murray.coon@aexp.com',
    'ayush.aman@aexp.com',
    'antoine.carter@aexp.com',
    'taylor.yip@aexp.com',
    'gabrielle.manturi@aexp.com',
    'david.schmidt@aexp.com',
    'michael.biedermann@aexp.com',
    'ryan.parish@aexp.com',
    'denise.mcdaniel@aexp.com',
    'errick.earl@aexp.com',
    'trenece.zamora@aexp.com',
    'ashley.rios@aexp.com',
    'ayushi.yadav@aexp.com',
    'jeff.morris@aexp.com',
    'eladio.jamar@aexp.com',
    'toni.mcdaniel@aexp.com',
    'christina.nguyen@aexp.com',
    'ty.mcmillan@aexp.com',
    'kristi.masters@aexp.com',
    'hannah.hayes@aexp.com',
    'amrin.gilani@aexp.com',
    'pranathi.balabhadrapatruni@aexp.com',
    'anita.tela@aexp.com',
    'morgan.obryant@aexp.com',
    'eladio.negron@aexp.com',
    'vonesa.karen@aexp.com',
    'christina.trinh@aexp.com',
    'shurawl.sibblies@aexp.com',
    'cassandra.walker@aexp.com',
    'alisha.chapman@aexp.com',
    'betina.gonzalez@aexp.com',
    'lilit.piramzadian@aexp.com',
    'scott.cohen@aexp.com',
    'susan.biondo@aexp.com',
    'georgina.vega@aexp.com',
    'felicia.ajala@aexp.com',
    'jeremiah.valera@aexp.com',
    'claire.kuhn@aexp.com',
    'hope.charity@aexp.com',
    'georgina.enriquez@aexp.com',
    'felicia.laughlin@aexp.com',
    'leslie.faulkner@aexp.com',
    'hannah.sacks@aexp.com',
    'frank.carmody@aexp.com',
    'florencia.dela@aexp.com',
    'shivani.shah@aexp.com',
    'krystal.cardamone@aexp.com',
    'terry.brooks@aexp.com',
    'caroline.croy@aexp.com',
    'roberta.willia@aexp.com',
    'miguel.herrera@aexp.com',
    'rahim.ewan@aexp.com',
    'ayush.gupta@aexp.com',
    'linda.warren@aexp.com',
    'gavin.thurlow@aexp.com',
    'florencia.serna@aexp.com',
    'cassidy.doss@aexp.com',
    'abigail.ngyuen@aexp.com',
    'natalie.cromer@aexp.com',
    'joanna.novick@aexp.com',
    'lho@paloaltonetworks.com',
    'jhall@paloaltonetworks.com',
    'laquino@paloaltonetworks.com',
    'ysaito@paloaltonetworks.com',
    'dshyam@paloaltonetworks.com',
    'ckerzner@paloaltonetworks.com',
    'asolis@paloaltonetworks.com',
    'jhunter@paloaltonetworks.com',
    'nnayak@paloaltonetworks.com',
    'pkrishnamurthy@paloaltonetworks.com',
    'jada@paloaltonetworks.com',
    'blyn@paloaltonetworks.com',
    'mbukich@paloaltonetworks.com',
    'hning@paloaltonetworks.com',
    'jjackson@paloaltonetworks.com',
    'reriksson@paloaltonetworks.com',
    'sthomas@paloaltonetworks.com',
    'anithya@paloaltonetworks.com',
    'labgrall@paloaltonetworks.com',
    'elee@paloaltonetworks.com',
    'kanchartechahar@paloaltonetworks.com',
    'lholden@paloaltonetworks.com',
    'kanthony@paloaltonetworks.com',
    'mann@paloaltonetworks.com',
    'jbatiste@paloaltonetworks.com',
    'ddee@paloaltonetworks.com',
    'bdiefenderfer@paloaltonetworks.com',
    'gmartin@paloaltonetworks.com',
    'echristianson@paloaltonetworks.com',
    'ddandrea@paloaltonetworks.com',
    'jflynn@paloaltonetworks.com',
    'gwillia@paloaltonetworks.com',
    'svan@paloaltonetworks.com',
    'mmyers@paloaltonetworks.com',
    'svooren@paloaltonetworks.com',
    'kjones@paloaltonetworks.com',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
  }
  return custom_set
# ------------------------ individual function end ------------------------
