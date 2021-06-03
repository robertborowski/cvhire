import psycopg2
from psycopg2 import Error

def select_company_quiz_settings_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id):
  print('=========================================== select_company_quiz_settings_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT * FROM triviafy_company_quiz_settings_slack_table WHERE company_quiz_settings_slack_workspace_team_id=%s AND company_quiz_settings_slack_channel_id=%s", [slack_workspace_team_id, slack_channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None:
      result_row = 'Company quiz settings do not exists in db table yet'
    
    print('returining result_row')
    print('=========================================== select_company_quiz_settings_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      print("Status: Company quiz settings do not exists in db table yet! ", error)
      print('=========================================== select_company_quiz_settings_function END ===========================================')
      return 'Company quiz settings do not exists in db table yet'