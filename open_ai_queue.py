# ------------------------ imports start ------------------------
import os, time
import openai
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
from website.backend.sql_queries import select_query_v1_function, select_query_v2_function, select_query_v3_function, select_query_v4_function, select_query_v5_function, update_query_v1_function, insert_query_v1_function
from website.backend.aws_logic import get_file_contents_from_aws_function
from website.backend.uploads_user import get_file_suffix_function
from website.backend.read_files import get_file_contents_function
from website.backend.open_ai_chatgpt import role_and_cv_grade_v1_function
from website.backend.sendgrid import send_email_template_function
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
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
      queue_results_arr_of_dicts = select_query_v1_function(postgres_cursor, 'requested')
      # ------------------------ select queue end ------------------------
      # ------------------------ if queue empty start ------------------------
      if len(queue_results_arr_of_dicts) == 0:
        # ------------------------ close db connection start ------------------------
        postgres_connect_close_function(postgres_connection, postgres_cursor)
        # ------------------------ close db connection end ------------------------
        # ------------------------ logs start ------------------------
        print('show queue empty')
        # ------------------------ logs end ------------------------
        time.sleep(60)
      # ------------------------ if queue empty end ------------------------
      else:
        # ------------------------ loop queue start ------------------------
        for i_queue_dict in queue_results_arr_of_dicts:
          # ------------------------ question type 1 start ------------------------
          if i_queue_dict['question_type'] == 'one-role-many-cvs':
            # ------------------------ get single start ------------------------
            role_dict_arr = select_query_v2_function(postgres_cursor, 'roles_obj', i_queue_dict['single_value'], i_queue_dict['fk_user_id'])
            role_dict = role_dict_arr[0]
            # ------------------------ get single end ------------------------
            # ------------------------ get multiple start ------------------------
            if i_queue_dict['multiple_values'] == 'select_all_ids':
              cvs_dict_arr = select_query_v4_function(postgres_cursor, 'cv_obj', i_queue_dict['fk_user_id'], 'active')
            else:
              cvs_dict_arr = select_query_v3_function(postgres_cursor, 'cv_obj', i_queue_dict['fk_user_id'], 'active', i_queue_dict['multiple_values'])
            # ------------------------ get multiple end ------------------------
            # ------------------------ loop multiple start ------------------------
            total_to_be_graded = len(cvs_dict_arr)
            total_graded_exists = 0
            for i_cv_dict in cvs_dict_arr:
              # ------------------------ check if grade already exists start ------------------------
              grade_exists = select_query_v5_function(postgres_cursor, role_dict['id'], i_cv_dict['id'], i_queue_dict['fk_user_id'])
              if len(grade_exists) != 0:
                total_graded_exists += 1
                # ------------------------ update db start ------------------------
                if total_graded_exists == total_to_be_graded:
                  update_query_v1_function(postgres_connection, postgres_cursor, 'graded', i_queue_dict['id'])
                # ------------------------ update db end ------------------------
                continue
              # ------------------------ check if grade already exists end ------------------------
              # ------------------------ if grade does not exists start ------------------------
              if len(grade_exists) == 0:
                # ------------------------ get content from aws start ------------------------
                i_cv_file_aws = get_file_contents_from_aws_function(i_cv_dict['cv_aws_id'])
                # ------------------------ get content from aws end ------------------------
                # ------------------------ get file suffix start ------------------------
                i_cv_file_format_suffix = get_file_suffix_function(i_cv_dict['cv_aws_id'])
                # ------------------------ get file suffix end ------------------------
                # ------------------------ read file contents start ------------------------
                i_cv_contents = get_file_contents_function(i_cv_file_aws, i_cv_file_format_suffix)
                # ------------------------ read file contents end ------------------------
                # ------------------------ open ai grading start ------------------------
                result_dict, open_ai_reply = role_and_cv_grade_v1_function(role_dict, i_cv_contents)
                # ------------------------ open ai grading end ------------------------
                # ------------------------ parse variables start ------------------------
                follow_ups_str = ''
                if type(result_dict['openai_follow_ups']) == list:
                  follow_ups_str = '~'.join(result_dict['openai_follow_ups'])
                else:
                  follow_ups_str = result_dict['openai_follow_ups']
                # ------------------------ parse variables end ------------------------
                # ------------------------ set variables start ------------------------
                id = create_uuid_function('grade_')
                created_timestamp = create_timestamp_function()
                fk_user_id = i_queue_dict['fk_user_id']
                status = 'valid'
                fk_role_id = role_dict['id']
                fk_cv_id = i_cv_dict['id']
                summary = result_dict['openai_summary']
                score = float(result_dict['openai_score'])
                follow_ups = follow_ups_str
                openai_response = open_ai_reply
                fk_ref_key = i_queue_dict['id']
                # ------------------------ set variables end ------------------------
                # ------------------------ insert to db start ------------------------
                insert_query_v1_function(postgres_connection, postgres_cursor, id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key)
                # ------------------------ insert to db end ------------------------
              # ------------------------ if grade does not exists end ------------------------
            # ------------------------ loop multiple end ------------------------
          # ------------------------ question type 1 end ------------------------
          # ------------------------ question type 2 start ------------------------
          elif i_queue_dict['question_type'] == 'one-cv-many-roles':
            # ------------------------ get single start ------------------------
            cv_dict_arr = select_query_v2_function(postgres_cursor, 'cv_obj', i_queue_dict['single_value'], i_queue_dict['fk_user_id'])
            cv_dict = cv_dict_arr[0]
            # ------------------------ get single end ------------------------
            # ------------------------ single cv only start ------------------------
            # ------------------------ get content from aws start ------------------------
            cv_file_aws = get_file_contents_from_aws_function(cv_dict['cv_aws_id'])
            # ------------------------ get content from aws end ------------------------
            # ------------------------ get file suffix start ------------------------
            cv_file_format_suffix = get_file_suffix_function(cv_dict['cv_aws_id'])
            # ------------------------ get file suffix end ------------------------
            # ------------------------ read file contents start ------------------------
            cv_contents = get_file_contents_function(cv_file_aws, cv_file_format_suffix)
            # ------------------------ read file contents end ------------------------
            # ------------------------ single cv only end ------------------------
            # ------------------------ get multiple start ------------------------
            if i_queue_dict['multiple_values'] == 'select_all_ids':
              roles_dict_arr = select_query_v4_function(postgres_cursor, 'roles_obj', i_queue_dict['fk_user_id'], 'open')
            else:
              roles_dict_arr = select_query_v3_function(postgres_cursor, 'roles_obj', i_queue_dict['fk_user_id'], 'open', i_queue_dict['multiple_values'])
            # ------------------------ get multiple end ------------------------
            # ------------------------ loop multiple start ------------------------
            total_to_be_graded = len(roles_dict_arr)
            total_graded_exists = 0
            for i_role_dict in roles_dict_arr:
              # ------------------------ check if grade already exists start ------------------------
              grade_exists = select_query_v5_function(postgres_cursor, i_role_dict['id'], cv_dict['id'], i_queue_dict['fk_user_id'])
              if len(grade_exists) != 0:
                total_graded_exists += 1
                # ------------------------ update db start ------------------------
                if total_graded_exists == total_to_be_graded:
                  update_query_v1_function(postgres_connection, postgres_cursor, 'graded', i_queue_dict['id'])
                # ------------------------ update db end ------------------------
                continue
              # ------------------------ check if grade already exists end ------------------------
              # ------------------------ if grade does not exists start ------------------------
              if len(grade_exists) == 0:
                # ------------------------ open ai grading start ------------------------
                result_dict, open_ai_reply = role_and_cv_grade_v1_function(i_role_dict, cv_contents)
                # ------------------------ open ai grading end ------------------------
                # ------------------------ parse variables start ------------------------
                follow_ups_str = ''
                if type(result_dict['openai_follow_ups']) == list:
                  follow_ups_str = '~'.join(result_dict['openai_follow_ups'])
                else:
                  follow_ups_str = result_dict['openai_follow_ups']
                # ------------------------ parse variables end ------------------------
                # ------------------------ set variables start ------------------------
                id = create_uuid_function('grade_')
                created_timestamp = create_timestamp_function()
                fk_user_id = i_queue_dict['fk_user_id']
                status = 'valid'
                fk_role_id = i_role_dict['id']
                fk_cv_id = cv_dict['id']
                summary = result_dict['openai_summary']
                score = float(result_dict['openai_score'])
                follow_ups = follow_ups_str
                openai_response = open_ai_reply
                fk_ref_key = i_queue_dict['id']
                # ------------------------ set variables end ------------------------
                # ------------------------ insert to db start ------------------------
                insert_query_v1_function(postgres_connection, postgres_cursor, id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key)
                # ------------------------ insert to db end ------------------------
              # ------------------------ if grade does not exists end ------------------------
            # ------------------------ loop multiple end ------------------------
          # ------------------------ question type 2 end ------------------------
        # ------------------------ loop queue end ------------------------
    except Exception as e:
      failure_counter += 1
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('CVHIRE_NOTIFICATIONS_EMAIL')
        output_subject = f'Exception error 001'
        output_body = f'failure_counter: {failure_counter} | Exception error 001: {e}'
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      # ------------------------ close db connection start ------------------------
      postgres_connect_close_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------