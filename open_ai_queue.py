# ------------------------ imports start ------------------------
import os, time
import openai
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
from website.backend.sql_queries import select_query_v1_function, select_query_v2_function, select_query_v3_function, select_query_v4_function, update_query_v1_function
from website.backend.aws_logic import get_file_contents_from_aws_function
from website.backend.uploads_user import get_file_suffix_function
from website.backend.read_files import get_file_contents_function
from website.backend.open_ai_chatgpt import role_and_cv_grade_v1_function
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
      print(' ------------- 0 ------------- ')
      # ------------------------ loop queue start ------------------------
      for i_queue_dict in queue_results_arr_of_dicts:
        # ------------------------ question type 1 start ------------------------
        if i_queue_dict['question_type'] == 'one-role-many-cvs':
          # ------------------------ get single start ------------------------
          role_dict_arr = select_query_v2_function(postgres_cursor, 'roles_obj', i_queue_dict['single_value'])
          role_dict = role_dict_arr[0]
          print(' ------------- 1 ------------- ')
          print(f"role_dict | type: {type(role_dict)} | {role_dict}")
          print(' ------------- 1 ------------- ')
          # ------------------------ get single end ------------------------
          # ------------------------ get multiple start ------------------------
          if i_queue_dict['multiple_values'] == 'select_all_ids':
            cv_dict_arr = select_query_v4_function(postgres_cursor, 'cv_obj', i_queue_dict['fk_user_id'])
          else:
            cv_dict_arr = select_query_v3_function(postgres_cursor, 'cv_obj', i_queue_dict['multiple_values'])
          # ------------------------ get multiple end ------------------------
          # ------------------------ loop cvs start ------------------------
          for i_cv_dict in cv_dict_arr:
            print(' ------------- 2 ------------- ')
            print(f"i_cv_dict | type: {type(i_cv_dict)} | {i_cv_dict}")
            print(' ------------- 2 ------------- ')
            # ------------------------ get content from aws start ------------------------
            i_file_aws = get_file_contents_from_aws_function(i_cv_dict['cv_aws_id'])
            # ------------------------ get content from aws end ------------------------
            # ------------------------ get file suffix start ------------------------
            file_format_suffix = get_file_suffix_function(i_cv_dict['cv_aws_id'])
            # ------------------------ get file suffix end ------------------------
            # ------------------------ read file contents start ------------------------
            cv_contents = get_file_contents_function(i_file_aws, file_format_suffix)
            # ------------------------ read file contents end ------------------------
            # ------------------------ open ai grading start ------------------------
            result = role_and_cv_grade_v1_function(role_dict, cv_contents)
            return True
            # ------------------------ open ai grading end ------------------------
          # ------------------------ loop cvs end ------------------------
          # ------------------------ update db start ------------------------
          # update_query_v1_function(postgres_connection, postgres_cursor, 'open_ai_queue_obj', 'status', 'closed')
          # ------------------------ update db end ------------------------
        # ------------------------ question type 1 end ------------------------
      # ------------------------ loop queue end ------------------------
      print(' ------------- 0 ------------- ')
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