# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error


# -------------------------------------------------------------- Main Function
def select_if_email_already_sent_expiring_id_function(postgres_connection, postgres_cursor, additional_input):
  print('=========================================== select_if_email_already_sent_expiring_id_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT \
                              * \
                            FROM \
                              candidates_email_sent_obj \
                            WHERE \
                              assessment_expiring_url_fk=%s;", [additional_input])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      print('=========================================== select_if_email_already_sent_expiring_id_function END ===========================================')
      return None

    print('=========================================== select_if_email_already_sent_expiring_id_function END ===========================================')
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      print('Except error hit: ', error)
      print('=========================================== select_if_email_already_sent_expiring_id_function END ===========================================')
      return None