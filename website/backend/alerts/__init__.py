# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_alert_message_function(redirect_var=None):
  alert_message_dict = {
      'message':'',
      'type':'danger'
    }
  if redirect_var == None:
    pass
  # ------------------------ errors start ------------------------
  elif redirect_var == 'e1':
    alert_message_dict = {
      'message':'Please enter a valid work email. No @gmail, @yahoo, etc.',
      'type':'danger'
    }
  elif redirect_var == 'e2':
    alert_message_dict = {
      'message':'Please enter a valid password.',
      'type':'danger'
    }
  elif redirect_var == 'e3':
    alert_message_dict = {
      'message':'Account already created for email',
      'type':'danger'
    }
  # ------------------------ errors end ------------------------
  # ------------------------ success start ------------------------
  elif redirect_var == 's1':
    alert_message_dict = {
      'message':'Request sent.',
      'type':'success'
    }
  elif redirect_var == 's2':
    alert_message_dict = {
      'message':'Schedule settings successfully updated. They will go into effect on your NEXT team quiz.',
      'type':'success'
    }
  # ------------------------ success end ------------------------
  # ------------------------ info end ------------------------
  elif redirect_var == 'i1':
    alert_message_dict = {
      'message':'Schedule settings unchanged.',
      'type':'info'
    }
  elif redirect_var == 'i2':
    alert_message_dict = {
      'message':'User is subscribed.',
      'type':'info'
    }
  # ------------------------ info end ------------------------
  # ------------------------ warning end ------------------------
  elif redirect_var == 'w1':
    alert_message_dict = {
      'message':'Deleted!',
      'type':'warning'
    }
  elif redirect_var == 'w2':
    alert_message_dict = {
      'message':'Poll successfully received',
      'type':'warning'
    }
  # ------------------------ warning end ------------------------
  # localhost_print_function('=========================================== alert_message_default_function_v2 END ===========================================')
  return alert_message_dict
# ------------------------ individual function end ------------------------
