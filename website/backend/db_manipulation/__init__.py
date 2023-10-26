# ------------------------ imports start ------------------------
from website.models import CvObj, LinkedinScrapeObj
from website.backend.static_lists import get_linkedin_identifiers_function, get_special_chars_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def additional_cv_info_from_db_function(current_user_id, input_dict):
  # ------------------------ get from db start ------------------------
  db_cv_obj = CvObj.query.filter_by(fk_user_id=current_user_id,id=input_dict['fk_cv_id']).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ if none start ------------------------
  if db_cv_obj == None:
    input_dict['candidate_name'] = ''
    input_dict['candidate_email'] = ''
    input_dict['candidate_phone'] = ''
    return input_dict
  # ------------------------ if none end ------------------------
  # ------------------------ pull data start ------------------------
  if db_cv_obj.candidate_name == None:
    input_dict['candidate_name'] = ''
  else:
    input_dict['candidate_name'] = db_cv_obj.candidate_name
  if db_cv_obj.candidate_email == None:
    input_dict['candidate_email'] = ''
  else:
    input_dict['candidate_email'] = db_cv_obj.candidate_email
  if db_cv_obj.candidate_phone == None:
    input_dict['candidate_phone'] = ''
  else:
    input_dict['candidate_phone'] = db_cv_obj.candidate_phone
  # ------------------------ pull data end ------------------------
  return input_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def form_scraped_emails_function():
  try:
    # ------------------------ pull from db start ------------------------
    db_objs = LinkedinScrapeObj.query.filter_by(completed=False).all()
    # ------------------------ pull from db end ------------------------
    counter = 0
    # ------------------------ loop start ------------------------
    print(' ------------- 0 ------------- ')
    for i_obj in db_objs:
      # # ------------------------ testing start ------------------------
      # counter += 1
      # if counter >= 100:
      #   break
      # # ------------------------ testing end ------------------------
      # ------------------------ clean display name start ------------------------
      display_name = i_obj.name.lower()
      display_name = remove_chars_after_first_comma_function(display_name)
      display_name = replace_chars_function(display_name)
      display_name = remove_identifiers_function(display_name)
      # ------------------------ clean display name end ------------------------
      print(f"display_name | type: {type(display_name)} | {display_name}")
    print(' ------------- 0 ------------- ')
    # ------------------------ loop end ------------------------
  except Exception as e:
    print(f'Error form_scraped_emails_function: {e}')
    pass
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def replace_chars_function(display_name):
  try:
    chars_dict = get_special_chars_function()
    # ------------------------ replace chars start ------------------------
    for k,v in chars_dict.items():
      try:
        display_name = display_name.replace(k,v)
      except:
        pass
    # ------------------------ replace chars end ------------------------
  except Exception as e:
    print(f'Error replace_chars_function: {e}')
  return display_name
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def remove_chars_after_first_comma_function(display_name):
  try:
    comma_index = display_name.find(',')
    if comma_index != -1:
      display_name = display_name[:comma_index]
  except Exception as e:
    print(f'Error remove_chars_after_first_comma_function: {e}')
  return display_name
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def remove_identifiers_function(display_name):
  try:
    # ------------------------ get arr of identifiers start ------------------------
    arr = get_linkedin_identifiers_function()
    # ------------------------ get arr of identifiers end ------------------------
    # ------------------------ replace occurences start ------------------------
    for i in arr:
      try:
        display_name = display_name.replace(i,'').strip()
      except:
        pass
    # ------------------------ replace occurences end ------------------------
  except Exception as e:
    print(f'Error remove_identifiers_function: {e}')
  return display_name
# ------------------------ individual function end ------------------------
