# ------------------------ imports start ------------------------
import os, time
import openai
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
from website.backend.sql_queries import sql_general_function
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
      # ------------------------ select start ------------------------
      results_arr_of_dicts = sql_general_function(postgres_cursor, 'latest_queue', 'open_ai_queue_obj')
      # ------------------------ select end ------------------------
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