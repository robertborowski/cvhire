# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.cached_login.check_if_user_login_through_cookies import check_if_user_login_through_cookies_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.get_upcoming_week_dates_data_dict import get_upcoming_week_dates_data_dict_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.utils.latest_quiz_utils.check_if_today_is_earlier_than_latest_quiz_start_date_utils.check_if_today_is_earlier_than_latest_quiz_start_date import check_if_today_is_earlier_than_latest_quiz_start_date_function
from backend.db.queries.select_queries.select_queries_triviafy_company_quiz_settings_slack_table.select_company_quiz_settings import select_company_quiz_settings_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.free_trial_period_utils.check_if_free_trial_period_is_expired_days_left import check_if_free_trial_period_is_expired_days_left_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.check_paid_latest_month_utils.check_if_user_team_channel_combo_paid_latest_month import check_if_user_team_channel_combo_paid_latest_month_function

# -------------------------------------------------------------- App Setup
quiz_pre_open_page_render_template = Blueprint("quiz_pre_open_page_render_template", __name__, static_folder="static", template_folder="templates")
@quiz_pre_open_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_pre_open_page_render_template.route("/dashboard/quiz/pre/open", methods=['GET','POST'])
def quiz_pre_open_page_render_template_function():
  localhost_print_function('=========================================== /dashboard/quiz/pre/open Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Page Pre Load Check - User Logged In Through Cookies START ------------------------
    # Check if user logged in through cookies
    user_nested_dict = check_if_user_login_through_cookies_function()
    # ------------------------ Page Pre Load Check - User Logged In Through Cookies END ------------------------

    # ------------------------ Page Pre Load Check - Redirect Check - Free Trial / Latest Month Paid START ------------------------
    # Check if user Team/Channel combo paid the latest month
    user_team_channeL_paid_latest_month = check_if_user_team_channel_combo_paid_latest_month_function(user_nested_dict)
    
    # If user's company did not pay latest month
    if user_team_channeL_paid_latest_month == False:
      # Check if user free trial is expired
      user_nested_dict = check_if_free_trial_period_is_expired_days_left_function(user_nested_dict)
      if user_nested_dict == None or user_nested_dict == True:
        return redirect('/subscription', code=302)

      days_left = str(user_nested_dict['trial_period_days_left_int']) + " days left."
      if user_nested_dict['trial_period_days_left_int'] == 1:
        days_left = str(user_nested_dict['trial_period_days_left_int']) + " day left."

      free_trial_ends_info = "Free Trial Ends: " + user_nested_dict['free_trial_end_date'] + ", " + days_left
    
    # If user's company did pay latest month
    if user_team_channeL_paid_latest_month == True:
      free_trial_ends_info = ''
    # ------------------------ Page Pre Load Check - Redirect Check - Free Trial / Latest Month Paid END ------------------------

    # ------------------------ Page Pre Load Check - Redirect Check - Permission Granted START ------------------------
    user_slack_email_permission_granted = user_nested_dict['user_slack_email_permission_granted']
    if user_slack_email_permission_granted == False or user_slack_email_permission_granted == 'False':
      return redirect('/notifications/email/permission', code=302)
    # ------------------------ Page Pre Load Check - Redirect Check - Permission Granted END ------------------------

    # ------------------------ Page Pre Load Check - Redirect Check - New User Questionnaire Answered START ------------------------
    user_slack_new_user_questionnaire_answered = user_nested_dict['user_slack_new_user_questionnaire_answered']
    if user_slack_new_user_questionnaire_answered == False or user_slack_new_user_questionnaire_answered == 'False':
      return redirect('/new/user/questionnaire', code=302)
    # ------------------------ Page Pre Load Check - Redirect Check - New User Questionnaire Answered END ------------------------
    
    
    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    slack_workspace_team_id = user_nested_dict['slack_team_id']
    slack_channel_id = user_nested_dict['slack_channel_id']


    # ------------------------ Double Check If Quiz Is Pre Open START ------------------------
    # ------------------------ Get Latest Quiz Data START ------------------------
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(user_nested_dict)
    if latest_company_quiz_object != None:
      # Assign the variables for the HTML inputs based on the pulled object
      uuid_quiz = latest_company_quiz_object[0]                                     # str
      quiz_timestamp_created = latest_company_quiz_object[1].strftime('%Y-%m-%d')   # str
      quiz_slack_team_id = latest_company_quiz_object[2]                            # str
      quiz_slack_channel_id = latest_company_quiz_object[3]                         # str
      quiz_start_date = latest_company_quiz_object[4].strftime('%Y-%m-%d')          # str
      quiz_start_day_of_week = latest_company_quiz_object[5]                        # str
      quiz_start_time = latest_company_quiz_object[6]                               # str
      quiz_end_date = latest_company_quiz_object[7].strftime('%Y-%m-%d')            # str
      quiz_end_day_of_week = latest_company_quiz_object[8]                          # str
      quiz_end_time = latest_company_quiz_object[9]                                 # str
      quiz_number_of_questions = latest_company_quiz_object[10]                     # int
      quiz_question_ids_str = latest_company_quiz_object[11]                        # str
      quiz_company_quiz_count = latest_company_quiz_object[12]                      # int

      # Quiz Question ID's have to be converted from 1 string to an arr
      quiz_question_ids_arr = convert_question_ids_from_string_to_arr_function(quiz_question_ids_str)   # list
    # ------------------------ Get Latest Quiz Data END ------------------------
    
    # ------------------------ Check Cannot View Created Quiz Before Start Date START ------------------------
    today_is_earlier_than_start_date = check_if_today_is_earlier_than_latest_quiz_start_date_function(quiz_start_day_of_week, quiz_start_time)
    if today_is_earlier_than_start_date != True:
      localhost_print_function('=========================================== /dashboard/quiz/pre/open Page END ===========================================')
      localhost_print_function('redirecting to quiz not yet open page')
      return redirect('/', code=302)
    # ------------------------ Check Cannot View Created Quiz Before Start Date END ------------------------
    # ------------------------ DDouble Check If Quiz Is Pre Open END ------------------------


    # ------------------------ Get The Company Quiz Settings START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    # Get quiz settings from DB as arr
    quiz_settings_arr = select_company_quiz_settings_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    # Assign the arr values
    company_quiz_settings_last_updated_timestamp = quiz_settings_arr[1]
    company_quiz_settings_start_day = quiz_settings_arr[2]
    company_quiz_settings_start_time = quiz_settings_arr[3]
    company_quiz_settings_end_day = quiz_settings_arr[4]
    company_quiz_settings_end_time = quiz_settings_arr[5]
    company_quiz_settings_questions_per_quiz = quiz_settings_arr[6]

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Get The Company Quiz Settings END ------------------------


    # ------------------------ Get Next Week's Dates Dict START ------------------------
    next_week_dates_dict = get_upcoming_week_dates_data_dict_function()

    company_quiz_start_day = company_quiz_settings_start_day
    company_quiz_start_date = next_week_dates_dict[company_quiz_start_day]
    # ------------------------ Get Next Week's Dates Dict End ------------------------

  except:
    localhost_print_function('page load except error hit')
    localhost_print_function('=========================================== /dashboard/quiz/pre/open Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /dashboard/quiz/pre/open Page END ===========================================')
  return render_template('dashboard_page_templates/quiz_pre_open_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          company_quiz_start_day_to_html = company_quiz_start_day,
                          company_quiz_settings_start_time_to_html = company_quiz_settings_start_time,
                          company_quiz_start_date_to_html = company_quiz_start_date,
                          free_trial_ends_info_to_html = free_trial_ends_info)