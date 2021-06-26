# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_latest_feedback_user_uuid_function(postgres_connection, postgres_cursor, user_uuid):
  localhost_print_function('=========================================== select_latest_feedback_user_uuid_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    # postgres_cursor.execute("SELECT DATE(MAX(quiz_feedback_timestamp)) FROM triviafy_quiz_feedback_responses_table WHERE quiz_feedback_user_uuid=%s", [user_uuid])
    postgres_cursor.execute("SELECT MAX(quiz_feedback_timestamp) FROM triviafy_quiz_feedback_responses_table WHERE quiz_feedback_user_uuid=%s", [user_uuid])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      return None
    
    localhost_print_function('=========================================== select_latest_feedback_user_uuid_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_latest_feedback_user_uuid_function END ===========================================')
      return None