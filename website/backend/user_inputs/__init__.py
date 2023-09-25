# ------------------------ imports start ------------------------
import re
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_company_name_function(ui_email):
  email_name = ''
  match = re.search(r'@([^\.]+)', ui_email)
  if match:
    email_name = match.group(1)
    email_name = email_name.capitalize()
  else:
    pass
  return email_name
# ------------------------ individual function end ------------------------
