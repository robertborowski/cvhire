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
      'message':'Company email only. No gmail, yahoo, .edu, etc.',
      'type':'danger'
    }
  elif redirect_var == 'e2':
    alert_message_dict = {
      'message':'Please enter a valid password.',
      'type':'danger'
    }
  elif redirect_var == 'e3':
    alert_message_dict = {
      'message':'Account already created for email, please login',
      'type':'danger'
    }
  elif redirect_var == 'e4':
    alert_message_dict = {
      'message':'Incorrect username/password.',
      'type':'danger'
    }
  elif redirect_var == 'e5':
    alert_message_dict = {
      'message':'You are not an admin',
      'type':'danger'
    }
  elif redirect_var == 'e6':
    alert_message_dict = {
      'message':'Invalid/lenghty full name',
      'type':'danger'
    }
  elif redirect_var == 'e7':
    alert_message_dict = {
      'message':'Error on upload',
      'type':'danger'
    }
  elif redirect_var == 'e8':
    alert_message_dict = {
      'message':'Inputs too long',
      'type':'danger'
    }
  elif redirect_var == 'e9':
    alert_message_dict = {
      'message':'Role name already exists',
      'type':'danger'
    }
  elif redirect_var == 'e10':
    alert_message_dict = {
      'message':'Invalid',
      'type':'danger'
    }
  elif redirect_var == 'e11':
    alert_message_dict = {
      'message':'Invalid file name',
      'type':'danger'
    }
  elif redirect_var == 'e12':
    alert_message_dict = {
      'message':'Download failed',
      'type':'danger'
    }
  elif redirect_var == 'e13':
    alert_message_dict = {
      'message':'Selection exceeded limit',
      'type':'danger'
    }
  elif redirect_var == 'e14':
    alert_message_dict = {
      'message':'You cannot edit a role after it has been graded against at least one CV',
      'type':'danger'
    }
  elif redirect_var == 'e15':
    alert_message_dict = {
      'message':'Your limit has been reached on the free plan. Please see account settings for subscription options.',
      'type':'danger'
    }
  elif redirect_var == 'e16':
    alert_message_dict = {
      'message':'Free plans cannot export results. Please see account settings for subscription options.',
      'type':'danger'
    }
  elif redirect_var == 'e17':
    alert_message_dict = {
      'message':'Free plans cannot upload company branding. Please see account settings for subscription options.',
      'type':'danger'
    }
  elif redirect_var == 'e18':
    alert_message_dict = {
      'message':'Free plans cannot edit results. Please see account settings for subscription options.',
      'type':'danger'
    }
  elif redirect_var == 'e19':
    alert_message_dict = {
      'message':'Individual input too long',
      'type':'danger'
    }
  elif redirect_var == 'e20':
    alert_message_dict = {
      'message':'Collective input too long',
      'type':'danger'
    }
  elif redirect_var == 'e21':
    alert_message_dict = {
      'message':'At least 1 follow up required',
      'type':'danger'
    }
  elif redirect_var == 'e22':
    alert_message_dict = {
      'message':'Email is already a user',
      'type':'danger'
    }
  elif redirect_var == 'e23':
    alert_message_dict = {
      'message':'Email is already scraped',
      'type':'danger'
    }
  elif redirect_var == 'e24':
    alert_message_dict = {
      'message':"Please create an account in order to access 'Account' and 'Settings'",
      'type':'danger'
    }
  elif redirect_var == 'e25':
    alert_message_dict = {
      'message':"Please create an account in order to access 'Export'",
      'type':'danger'
    }
  elif redirect_var == 'e26':
    alert_message_dict = {
      'message':"Job description generator coming soon.",
      'type':'danger'
    }
  # ------------------------ errors end ------------------------
  # ------------------------ success start ------------------------
  elif redirect_var == 's1':
    alert_message_dict = {
      'message':'Account locked',
      'type':'success'
    }
  elif redirect_var == 's2':
    alert_message_dict = {
      'message':'Added to db',
      'type':'success'
    }
  elif redirect_var == 's3':
    alert_message_dict = {
      'message':'Email sent',
      'type':'success'
    }
  elif redirect_var == 's4':
    alert_message_dict = {
      'message':'Successfully created',
      'type':'success'
    }
  elif redirect_var == 's5':
    alert_message_dict = {
      'message':'Successfully updated',
      'type':'success'
    }
  elif redirect_var == 's6':
    alert_message_dict = {
      'message':'Successfully deleted',
      'type':'success'
    }
  elif redirect_var == 's7':
    alert_message_dict = {
      'message':'Successfully uploaded file(s)',
      'type':'success'
    }
  elif redirect_var == 's8':
    alert_message_dict = {
      'message':'Export in progress. We will send the .csv file to your email.',
      'type':'success'
    }
  elif redirect_var == 's9':
    alert_message_dict = {
      'message':'Thank you! We will get back to you shortly.',
      'type':'success'
    }
  elif redirect_var == 's10':
    alert_message_dict = {
      'message':'Successfully verified',
      'type':'success'
    }
  elif redirect_var == 's11':
    alert_message_dict = {
      'message':'Successfully subscribed',
      'type':'success'
    }
  elif redirect_var == 's12':
    alert_message_dict = {
      'message':'Successfully added',
      'type':'success'
    }
  elif redirect_var == 's13':
    alert_message_dict = {
      'message':'Successfully scraped',
      'type':'success'
    }
  # ------------------------ success end ------------------------
  # ------------------------ info end ------------------------
  elif redirect_var == 'i1':
    alert_message_dict = {
      'message':'No change',
      'type':'info'
    }
  elif redirect_var == 'i2':
    alert_message_dict = {
      'message':'Already exists in db',
      'type':'info'
    }
  elif redirect_var == 'i3':
    alert_message_dict = {
      'message':'Loading...',
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
