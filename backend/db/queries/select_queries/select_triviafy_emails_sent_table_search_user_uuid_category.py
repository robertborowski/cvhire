# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_emails_sent_table_search_user_uuid_category_function(postgres_connection, postgres_cursor, user_uuid, email_sent_search_category, uuid_quiz):
  localhost_print_function('=========================================== select_triviafy_emails_sent_table_search_user_uuid_category_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT * FROM triviafy_emails_sent_table WHERE email_sent_to_user_uuid_fk=%s AND email_sent_category=%s AND email_sent_quiz_uuid_fk=%s", [user_uuid, email_sent_search_category, uuid_quiz])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_emails_sent_table_search_user_uuid_category_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_triviafy_emails_sent_table_search_user_uuid_category_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_emails_sent_table_search_user_uuid_category_function END ===========================================')
      return None