# ------------------------ imports start ------------------------
from sqlalchemy import and_
from website.models import CvObj, LinkedinScrapeObj, CompanyInfoObj, EmailScrapedObj, EmailSentObj
from website.backend.static_lists import get_linkedin_identifiers_function, get_special_chars_function
import re
from website import db
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.static_lists import get_emails_to_delete_function
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
    # ------------------------ loop start ------------------------
    for i_obj in db_objs:
      # ------------------------ clean display name start ------------------------
      display_name = i_obj.name.lower()
      display_name = remove_chars_after_first_comma_function(display_name)
      display_name = replace_chars_function(display_name)
      display_name = remove_identifiers_function(display_name)
      display_name = remove_emojis_function(display_name)
      display_name = display_name.strip()
      # ------------------------ clean display name end ------------------------
      # ------------------------ get first name and potential last names arr start ------------------------
      first_name, potential_last_names_arr = derive_names_function(display_name)
      # ------------------------ get first name and potential last names arr end ------------------------
      # ------------------------ if skip start ------------------------
      if first_name == 'skip':
        i_obj.completed = True
        db.session.commit()
        continue
      # ------------------------ if skip end ------------------------
      # ------------------------ form potential emails start ------------------------
      form_potential_emails_function(first_name, potential_last_names_arr, i_obj)
      # ------------------------ form potential emails end ------------------------
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

# ------------------------ individual function start ------------------------
def remove_emojis_function(display_name):
  try:
    # Unicode ranges for emojis
    emoji_pattern = re.compile("["
      u"\U0001F600-\U0001F64F"  # emoticons
      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
      u"\U0001F680-\U0001F6FF"  # transport & map symbols
      u"\U0001F700-\U0001F77F"  # alchemical symbols
      u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
      u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
      u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
      u"\U0001FA00-\U0001FA6F"  # Chess Symbols
      u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
      u"\U00002702-\U000027B0"  # Dingbats
      u"\U000024C2-\U0001F251"  # Enclosed Characters
      "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', display_name)
  except Exception as e:
    print(f'Error remove_emojis_function: {e}')
  return display_name
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def derive_names_function(display_name):
  try:
    arr = display_name.split(' ')
    # ------------------------ skip check start ------------------------
    if len(arr) == 1:
      return 'skip', 'skip'
    # ------------------------ skip check end ------------------------
    # ------------------------ set first name and potential last name arr start ------------------------
    first_name = arr[0]
    potential_last_names_arr = arr[1:]
    # ------------------------ set first name and potential last name arr end ------------------------
    # ------------------------ last name arr is only len 1 and 1 letter check start ------------------------
    if len(potential_last_names_arr) == 1 and len(potential_last_names_arr[0]) == 1:
      return 'skip', 'skip'
    # ------------------------ last name arr is only len 1 and 1 letter check end ------------------------
    # ------------------------ remove any 1 letter potential last names/middle initials start ------------------------
    for i in range(len(potential_last_names_arr) - 1, -1, -1):
      if len(potential_last_names_arr[i]) == 1:
        del potential_last_names_arr[i]
    # ------------------------ remove any 1 letter potential last names/middle initials end ------------------------
    # ------------------------ remove any obvious not last names start ------------------------
    exceptions_arr = ['jr','dj','cj','mo','ii','iii','iv','robert','pc']
    for i in range(len(potential_last_names_arr) - 1, -1, -1):
      if potential_last_names_arr[i] in exceptions_arr:
        del potential_last_names_arr[i]
    # ------------------------ remove any obvious not last names end ------------------------
    # ------------------------ special case, combine two part last names like LaTorres, DelVecchio, etc start ------------------------
    exceptions_arr = ['la','de','el']
    i = 0
    while i < len(potential_last_names_arr) - 1:
      if potential_last_names_arr[i] in exceptions_arr:
        potential_last_names_arr[i] = potential_last_names_arr[i] + potential_last_names_arr[i+1]
        del potential_last_names_arr[i+1]
      else:
        i += 1
    # ------------------------ special case, combine two part last names like LaTorres, DelVecchio, etc end ------------------------
    # ------------------------ last name arr is only len 1 and 1 letter check start ------------------------
    if potential_last_names_arr == []:
      return 'skip', 'skip'
    # ------------------------ last name arr is only len 1 and 1 letter check end ------------------------
  except Exception as e:
    print(f'Error derive_names_function: {e}')
  return first_name, potential_last_names_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def form_potential_emails_function(first_name, potential_last_names_arr, i_linkedin_obj):
  # ------------------------ get company url start ------------------------
  db_company_obj = CompanyInfoObj.query.filter_by(name=i_linkedin_obj.company).first()
  # ------------------------ get company url end ------------------------
  try:
    for i_last_name in potential_last_names_arr:
      emails_arr = []
      # ------------------------ email formats start ------------------------
      emails_arr.append(first_name + '.' + i_last_name) # First.Last
      emails_arr.append(first_name + i_last_name) # FirstLast
      emails_arr.append(first_name[0] + i_last_name) # FLast
      emails_arr.append(first_name[0] + '.' + i_last_name) # F.Last
      emails_arr.append(first_name) # First
      emails_arr.append(first_name + i_last_name[0]) # FirstL
      emails_arr.append(first_name + '_' + i_last_name) # First_Last
      # ------------------------ email formats end ------------------------
      # ------------------------ arr to str start ------------------------
      emails_str = '~'.join(emails_arr)
      # ------------------------ arr to str end ------------------------
      # ------------------------ check if emails exist start ------------------------
      db_email_obj = EmailScrapedObj.query.filter_by(all_formats=emails_str,website_address=db_company_obj.url).first()
      if db_email_obj != None and db_email_obj != []:
        pass
      # ------------------------ check if emails exist end ------------------------
      else:
        # ------------------------ add to db start ------------------------
        try:
          new_row = EmailScrapedObj(
            id=create_uuid_function('scrape_'),
            created_timestamp=create_timestamp_function(),
            all_formats=emails_str,
            correct_format=None,
            website_address=db_company_obj.url,
            unsubscribed=False
          )
          db.session.add(new_row)
          i_linkedin_obj.completed = True
          db.session.commit()
        except:
          pass
        # ------------------------ add to db end ------------------------
  except Exception as e:
    print(f'Error form_potential_emails_function: {e}')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def delete_from_scraped_emails_function():
  # ------------------------ get set start ------------------------
  email_set = get_emails_to_delete_function()
  # ------------------------ get set end ------------------------
  # ------------------------ set variables start ------------------------
  change_occurred = False
  # ------------------------ set variables end ------------------------
  for i_email in email_set:
    # # ------------------------ delete from emails sent table start ------------------------
    # EmailSentObj.query.filter_by(to_email=i_email).delete()
    # # ------------------------ delete from emails sent table end ------------------------
    email_arr = i_email.split('@')
    # ------------------------ search db start ------------------------
    db_scrape_obj = EmailScrapedObj.query.filter(and_(EmailScrapedObj.all_formats.like(f'%{email_arr[0]}%'), EmailScrapedObj.website_address == email_arr[1])).first()
    # ------------------------ search db end ------------------------
    # ------------------------ check for change start ------------------------
    if db_scrape_obj != None and db_scrape_obj != []:
      # ------------------------ delete row from db start ------------------------
      EmailScrapedObj.query.filter_by(id=db_scrape_obj.id).delete()
      # ------------------------ delete row from db end ------------------------
      if change_occurred == False:
        change_occurred = True
    # ------------------------ check for change end ------------------------
  # ------------------------ if change occurred, save start ------------------------
  if change_occurred == True:
    db.session.commit()
  # ------------------------ if change occurred, save end ------------------------
  return True
# ------------------------ individual function end ------------------------
