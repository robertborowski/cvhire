# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.cached_login.check_if_user_login_through_cookies import check_if_user_login_through_cookies_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_payment_admins_with_email import select_triviafy_user_login_information_table_slack_all_payment_admins_with_email_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- App Setup
subscription_index_page_render_template = Blueprint("subscription_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@subscription_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@subscription_index_page_render_template.route("/subscription", methods=['GET','POST'])
def subscription_index_page_render_template_function():
  localhost_print_function('=========================================== /subscription Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Page Pre Load Check - User Logged In Through Cookies START ------------------------
    # Check if user logged in through cookies
    user_nested_dict = check_if_user_login_through_cookies_function()
    # ------------------------ Page Pre Load Check - User Logged In Through Cookies END ------------------------
    

    # ------------------------ Page Pre Load Check - Redirect Check - Permission Granted START ------------------------
    user_slack_email_permission_granted = user_nested_dict['user_slack_email_permission_granted']
    if user_slack_email_permission_granted == False or user_slack_email_permission_granted == 'False':
      return redirect('/notifications/email/permission', code=302)
    # ------------------------ Page Pre Load Check - Redirect Check - Permission Granted END ------------------------


    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['slack_channel_name']
    # ------------------------ Page Company Info END ------------------------

    # ------------------------ Get Variables From User Nested Dict START ------------------------
    user_payment_admin_status = user_nested_dict['user_is_payment_admin']
    slack_workspace_team_id = user_nested_dict['slack_team_id']
    slack_channel_id = user_nested_dict['slack_channel_id']
    # ------------------------ Get Variables From User Nested Dict END ------------------------


    # ------------------------ Connect to DB START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # ------------------------ Connect to DB END ------------------------


    # ------------------------ SQL Pull Data START ------------------------
    all_team_payment_admins_arr = select_triviafy_user_login_information_table_slack_all_payment_admins_with_email_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    
    all_team_payment_admin_emails_arr = []
    for i in all_team_payment_admins_arr:
      all_team_payment_admin_emails_arr.append(i[2])
    # ------------------------ SQL Pull Data END ------------------------


    # ------------------------ Close Connection to DB START ------------------------
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Close Connection to DB END ------------------------    
    
  except:
    localhost_print_function('page load except error hit')
    localhost_print_function('=========================================== /subscription Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /subscription Page END ===========================================')
  return render_template('subscription_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_payment_admin_status_html = user_payment_admin_status,
                          all_team_payment_admin_emails_arr_to_html = all_team_payment_admin_emails_arr)