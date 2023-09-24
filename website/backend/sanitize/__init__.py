# ------------------------ imports start ------------------------
import re
from website.backend.static_lists import get_list_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_email_function(user_input_email, is_signup='false'):
  desired_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if(re.fullmatch(desired_regex_pattern, user_input_email)):
    # ------------------------ signup specific function start ------------------------
    if is_signup == 'true':
      blocked_email_arr = get_list_function('blocked_email_arr')
      for i_email in blocked_email_arr:
        if i_email in user_input_email.lower():
          return False
    # ------------------------ signup specific function end ------------------------
    return user_input_email
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_password_function(user_input_password):
  if len(user_input_password) > 150 or len(user_input_password) < 4:
    return False
  return user_input_password
# ------------------------ individual function end ------------------------