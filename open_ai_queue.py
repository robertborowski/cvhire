# ------------------------ imports start ------------------------
import os, time
import openai
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
from website.backend.sql_queries import select_query_v1_function, select_query_v2_function, select_query_v3_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def run_function():
  queue_on = True
  failure_counter = 0
  while queue_on == True:
    # ------------------------ infinite loop break start ------------------------
    if failure_counter >= 5:
      queue_on == False
    # ------------------------ infinite loop break end ------------------------
    try:
      # ------------------------ open db connection start ------------------------
      postgres_connection, postgres_cursor = postgres_connect_open_function()
      # ------------------------ open db connection end ------------------------
      # ------------------------ select queue start ------------------------
      queue_results_arr_of_dicts = select_query_v1_function(postgres_cursor, 'open_ai_queue_obj')
      # ------------------------ select queue end ------------------------
      # ------------------------ loop db rows start ------------------------
      for i_queue_dict in queue_results_arr_of_dicts:
        # ------------------------ question type 1 start ------------------------
        if i_queue_dict['question_type'] == 'one-role-many-cvs':
          # ------------------------ get single start ------------------------
          role_dict_arr = select_query_v2_function(postgres_cursor, 'roles_obj', i_queue_dict['single_value'])
          role_dict = role_dict_arr[0]
          # ------------------------ get single end ------------------------
          # ------------------------ get multiple start ------------------------
          cv_dict_arr = select_query_v3_function(postgres_cursor, 'cv_obj', i_queue_dict['multiple_values'])
          print(' ------------- 0 ------------- ')
          print(f"cv_dict_arr | type: {type(cv_dict_arr)} | {cv_dict_arr}")
          print(' ------------- 0 ------------- ')
          # ------------------------ get multiple end ------------------------
        # ------------------------ question type 1 end ------------------------
      # ------------------------ loop db rows end ------------------------
      # ------------------------ close db connection start ------------------------
      postgres_connect_close_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
      # ------------------------ if yes results end ------------------------
    except Exception as e:
      print(f'Error: {e}')
      failure_counter += 1
      pass
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------