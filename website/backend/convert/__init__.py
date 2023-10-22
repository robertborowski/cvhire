# ------------------------ imports start ------------------------
from website.backend.static_lists import get_stars_img_function
import datetime
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def convert_obj_row_to_dict_function(row):
  return {c.name: getattr(row, c.name) for c in row.__table__.columns}
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def objs_to_arr_of_dicts_function(db_obj, identifier=None):
  arr = []
  # ------------------------ variables for radios and checkboxes start ------------------------
  i_counter = 0
  # ------------------------ variables for radios and checkboxes end ------------------------
  for i_obj in db_obj:
    # ------------------------ variables for radios and checkboxes start ------------------------
    i_counter += 1
    # ------------------------ variables for radios and checkboxes end ------------------------
    i_dict = convert_obj_row_to_dict_function(i_obj)
    # ------------------------ additional details start ------------------------
    if identifier == 'roles':
      char_limit = 35
      i_dict['name_display'] = i_dict['name'][:char_limit]
      # ------------------------ variables for radios and checkboxes start ------------------------
      i_dict['roles_count_id'] = 'radio_count_' + str(i_counter)
      # ------------------------ variables for radios and checkboxes end ------------------------
    # ------------------------ additional details end ------------------------
    # ------------------------ additional details start ------------------------
    if identifier == 'cv':
      # ------------------------ variables for radios and checkboxes start ------------------------
      i_dict['cv_count_id'] = 'checkbox_count_' + str(i_counter)
      # ------------------------ variables for radios and checkboxes end ------------------------
      char_limit = 30
      i_dict['cv_upload_name_display'] = i_dict['cv_upload_name'][:char_limit]
      try:
        i_dict['candidate_email_display'] = i_dict['candidate_email'][:char_limit]
      except:
        pass
      try:
        i_dict['candidate_name_display'] = i_dict['candidate_name'][:char_limit]
      except:
        pass
      try:
        i_dict['candidate_phone_display'] = i_dict['candidate_phone'][:char_limit]
      except:
        pass
    # ------------------------ additional details end ------------------------
    # ------------------------ additional details start ------------------------
    if identifier == 'results':
      char_limit = 35
      i_dict['fk_role_name_display'] = i_dict['fk_role_name'][:char_limit]
      i_dict['fk_cv_name_display'] = i_dict['fk_cv_name'][:char_limit]
      # ------------------------ star images start ------------------------
      i_dict = get_stars_img_function(i_dict)
      # ------------------------ star images end ------------------------
    # ------------------------ additional details end ------------------------
    # ------------------------ additional details start ------------------------
    if identifier == 'blog':
      i_dict['title_read'] = i_dict['title'].replace("-", " ")
      i_dict['keywords_read'] = keywords_present_function(i_dict['keywords'])
      i_dict['created_timestamp_read'] = timestamp_to_date_function(i_dict['created_timestamp'])
    # ------------------------ additional details end ------------------------
    arr.append(i_dict)
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_follow_ups_function(db_dict):
  arr = []
  try:
    arr = db_dict['follow_ups'].split('~')
    # ------------------------ counter start ------------------------
    index = -1
    counter = 0
    for i_str in arr:
      index += 1
      counter += 1
      count_str = str(counter) + '.'
      if count_str not in i_str[:10]:
        arr[index] = count_str + ' ' + i_str
    # ------------------------ counter end ------------------------
  except Exception as e:
    pass
  return arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_follow_ups_dict_function(db_dict):
  i_dict = {}
  try:
    arr = db_dict['follow_ups'].split('~')
    # ------------------------ loop create dict start ------------------------
    for i in range(0, 10):
      i_dict[str(i+1)] = {}
      i_dict[str(i+1)]['num'] = str(i+1)
      i_dict[str(i+1)]['ui'] = ''
      try:
        i_dict[str(i+1)]['ui'] = arr[i]
      except:
        pass
    # ------------------------ loop create dict end ------------------------
  except Exception as e:
    pass
  return i_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def keywords_present_function(input_str):
  arr_upper = []
  try:
    arr = input_str.split('~')
    for i in arr:
      arr_upper.append(i.upper())
  except Exception as e:
    pass
  return arr_upper
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def timestamp_to_date_function(input_datetime):
  formatted_date = None
  try:
    formatted_date = input_datetime.strftime('%Y-%m-%d')
  except Exception as e:
    pass
  return formatted_date
# ------------------------ individual function end ------------------------
