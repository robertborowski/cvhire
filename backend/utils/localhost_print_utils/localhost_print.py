# -------------------------------------------------------------- Imports
import os


# -------------------------------------------------------------- Main Function
def localhost_print_function(input_value_to_print):
  server_env = os.environ.get('TESTING', 'false')
  
  if server_env and (server_env == 'false' or server_env == 'true'):
    print(input_value_to_print)
  
  return None