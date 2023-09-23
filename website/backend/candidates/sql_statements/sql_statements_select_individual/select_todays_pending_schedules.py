# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error


# -------------------------------------------------------------- Main Function
def select_todays_pending_schedules_function(postgres_connection, postgres_cursor, additional_input):
  print('=========================================== select_todays_pending_schedules_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT \
                              * \
                            FROM \
                              candidates_schedule_obj \
                            WHERE \
                              candidate_status='Pending' AND \
                              send_date<=%s;", [additional_input])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      print('=========================================== select_todays_pending_schedules_function END ===========================================')
      return None

    print('=========================================== select_todays_pending_schedules_function END ===========================================')
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      print('Except error hit: ', error)
      print('=========================================== select_todays_pending_schedules_function END ===========================================')
      return None