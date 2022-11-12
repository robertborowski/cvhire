# -------------------------------------------------------------- Imports
from flask import Blueprint, redirect, request
import os
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.sanitize_user_inputs.sanitize_collect_email import sanitize_collect_email_function
from backend.utils.sanitize_user_inputs.sanitize_collect_name import sanitize_collect_name_function
from backend.utils.sanitize_user_inputs.sanitize_collect_job_title import sanitize_collect_job_title_function
from backend.db.queries.select_queries.select_queries_triviafy_landing_page_emails_collection_table.select_if_email_collected_exists_candidates import select_if_email_collected_exists_candidates_function
from backend.db.queries.insert_queries.insert_queries_triviafy_landing_page_emails_collection_table.insert_user_collected_email_candidates import insert_user_collected_email_candidates_function
from backend.db.queries.insert_queries.insert_queries_triviafy_emails_sent_table.insert_triviafy_emails_sent_table import insert_triviafy_emails_sent_table_function

# -------------------------------------------------------------- App Setup
collect_email_processing_candidates = Blueprint("collect_email_processing_candidates", __name__, static_folder="static", template_folder="templates")
@collect_email_processing_candidates.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@collect_email_processing_candidates.route("/candidates/email", methods=['GET','POST'])
def collect_email_processing_candidates_function():
  localhost_print_function('=========================================== /candidates/email Page START ===========================================')


  # ------------------------ Sanitize user inputs START ------------------------
  try:
    # Get/sanitize user inputs from form
    user_form_input_email = sanitize_collect_email_function(request.form.get('user_input_email'))

  except:
    localhost_print_function('invalid url')
    localhost_print_function('=========================================== /candidates/email Page END ===========================================')
    return redirect('/', code=302)
  # ------------------------ Sanitize user inputs END ------------------------


  # ------------------------ Check sanitized results START ------------------------
  # Check if sanitized inputs are valid and if code can move on
  if user_form_input_email == None:
    localhost_print_function('invalid inputs')
    localhost_print_function('=========================================== /candidates/email Page END ===========================================')
    return redirect('/', code=302)
  # ------------------------ Check sanitized results END ------------------------


  # ------------------------ connect to db start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ connect to db end ------------------------


  # ------------------------ Check If Email Already in DB START ------------------------
  email_collected_exists = select_if_email_collected_exists_candidates_function(postgres_connection, postgres_cursor, user_form_input_email)
  if email_collected_exists != None:
    localhost_print_function('email already exists in DB')
    localhost_print_function('=========================================== /candidates/email Page END ===========================================')
    return redirect('/candidates/email/success', code=302)
  # ------------------------ Check If Email Already in DB END ------------------------


  # ------------------------ Declare database variables START ------------------------
  # Additional variables for database
  collect_email_uuid = create_uuid_function('collect_email_')
  collect_email_timestamp = create_timestamp_function()
  # ------------------------ Declare database variables END ------------------------


  # ------------------------ Insert into DB START ------------------------
  output_message = insert_user_collected_email_candidates_function(postgres_connection, postgres_cursor, collect_email_uuid, collect_email_timestamp, user_form_input_email)
  # ------------------------ Insert into DB END ------------------------

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Upload Question to database END ------------------------

  
  localhost_print_function('=========================================== /candidates/email Page END ===========================================')
  return redirect('/candidates/email/success', code=302)