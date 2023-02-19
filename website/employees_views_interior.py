# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.backend.candidates.browser import browser_response_set_cookie_function_v4
from website.models import EmployeesGroupsObj, EmployeesGroupSettingsObj, EmployeesTestsObj, EmployeesDesiredCategoriesObj, CreatedQuestionsObj, EmployeesTestsGradedObj
from website.backend.candidates.autogeneration import generate_random_length_uuid_function, question_choices_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function, convert_timestamp_to_month_day_string_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.string_manipulation import all_employee_question_categories_sorted_function
from website.backend.candidates.user_inputs import sanitize_char_count_1_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website.backend.candidates.quiz import create_quiz_function, grade_quiz_function
import json
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_interior = Blueprint('employees_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/dashboard')
@employees_views_interior.route('/employees/dashboard/<url_redirect_code>')
@login_required
def login_dashboard_page_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ login_dashboard_page_function START ------------------------ ')
  # ------------------------ auto redirect checks start ------------------------
  """
  -The code will always hit this dashboard on login or create account. BUT BEFORE setting the cookie on the browser, we are going to auto redirect
  users this makes the UX better so they dont have to click, read, or think, just auto redirect. The downside is that you cannot set the cookie
  unless you know for sure where the user is ending up. So the redirected page will ALSO have to include the function that sets the cookie.
  Downside is repeating code but it is not for all pages, only for the pages that auto redirect on new account creation.
  -These pages will require the template_location_url variable
  """
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'employees/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  # ------------------------ pull/create group id start ------------------------
  company_group_id = None
  db_groups_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
  if db_groups_obj == None or db_groups_obj == []:
    company_group_id = generate_random_length_uuid_function(6)
    # ------------------------ while loop if generated group id already exists start ------------------------
    group_id_exists_check = EmployeesGroupsObj.query.filter_by(public_group_id=company_group_id).first()
    while group_id_exists_check != None:
      company_group_id = generate_random_length_uuid_function(6)
      group_id_exists_check = EmployeesGroupsObj.query.filter_by(public_group_id=company_group_id).first()
    # ------------------------ while loop if generated group id already exists end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = EmployeesGroupsObj(
        id = create_uuid_function('group_'),
        created_timestamp = create_timestamp_function(),
        fk_company_name = current_user.company_name,
        fk_user_id = current_user.id,
        public_group_id = company_group_id,
        status = 'active'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
  else:
    company_group_id = db_groups_obj.public_group_id
  # ------------------------ pull/create group id end ------------------------
  # ------------------------ pull/create group settings start ------------------------
  db_group_settings_obj = EmployeesGroupSettingsObj.query.filter_by(fk_group_id=company_group_id).first()
  if db_group_settings_obj == None or db_group_settings_obj == []:
    # ------------------------ insert to db start ------------------------
    try:
      new_row = EmployeesGroupSettingsObj(
        id = create_uuid_function('gset_'),
        created_timestamp = create_timestamp_function(),
        fk_group_id = company_group_id,
        fk_user_id = current_user.id,
        timezone = 'EST',
        start_day = 'Monday',
        start_time = '12 PM',
        end_day = 'Thursday',
        end_time = '1 PM',
        cadence = 'Weekly',
        total_questions = 10,
        question_type = 'Mixed',
        categories = 'all_categories'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
  else:
    pass
  # ------------------------ pull/create group settings end ------------------------
  # ------------------------ pull/create latest test start ------------------------
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  first_test_exists = False
  if db_tests_obj == None or db_tests_obj == []:
    pass
  else:
    first_test_exists = True
    # ------------------------ create latest test start ------------------------
    create_quiz_status = create_quiz_function(db_group_settings_obj.fk_group_id)
    # ------------------------ create latest test end ------------------------
    # ------------------------ latest test info start ------------------------
    db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
    start_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.start_timestamp)
    end_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.end_timestamp)
    page_dict['full_time_string'] = start_month_day_str + ', ' + db_tests_obj.start_time + ' - ' + end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
    page_dict['ending_time_string'] = end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
    # ------------------------ latest test info end ------------------------
  page_dict['first_test_exists'] = first_test_exists
  # ------------------------ pull/create latest test end ------------------------
  # ------------------------ pull latest graded start ------------------------
  ui_latest_test_completed = False
  try:
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=db_tests_obj.id, fk_user_id=current_user.id).first()
    if db_test_grading_obj.status == 'complete':
      ui_latest_test_completed = True
  except:
    pass
  page_dict['ui_latest_test_completed'] = ui_latest_test_completed
  # ------------------------ pull latest graded end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, alert_message_dict_to_html=alert_message_dict, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v4(current_user, template_location_url, alert_message_dict, page_dict)
    localhost_print_function(' ------------------------ login_dashboard_page_function END ------------------------ ')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/request', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/request/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_categories_request_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_categories_request_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ if post method hit start ------------------------
  ui_requested = ''
  if request.method == 'POST':
    ui_requested = request.form.get('ui_requested')
    ui_requested = sanitize_char_count_1_function(ui_requested)
    if ui_requested == False:
      return redirect(url_for('employees_views_interior.employees_categories_request_function', url_redirect_code='e5'))
    else:
      # ------------------------ create new user in db start ------------------------
      insert_new_row = EmployeesDesiredCategoriesObj(
        id=create_uuid_function('cat_'),
        created_timestamp=create_timestamp_function(),
        user_id_fk=current_user.id,
        desired_categories=ui_requested
      )
      db.session.add(insert_new_row)
      db.session.commit()
      # ------------------------ create new user in db end ------------------------
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
        output_subject = f'Triviafy - Employees Requested Category - {current_user.email}'
        output_body = f"Hi there,\n\nRequester: {current_user.email}\nRequested: '{ui_requested}'\n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('employees_views_interior.employees_categories_request_function', url_redirect_code='s1'))
  # ------------------------ if post method hit end ------------------------
  localhost_print_function(' ------------------------ employees_categories_request_function END ------------------------ ')
  return render_template('employees/interior/request_categories/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/schedule', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/schedule/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_schedule_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_schedule_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current group settings start ------------------------
  user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
  db_group_settings_obj = EmployeesGroupSettingsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesGroupSettingsObj.created_timestamp.desc()).first()
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  page_dict['db_group_settings_dict'] = db_group_settings_dict
  page_dict['weekdays'], page_dict['times'], page_dict['timezones'] = days_times_timezone_arr_function()
  page_dict['quiz_cadence_arr'], page_dict['question_num_arr'], page_dict['question_type_arr'] = question_choices_function()
  # ------------------------ get current group settings end ------------------------
  # ------------------------ pull/create latest test start ------------------------
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  first_test_exists = False
  if db_tests_obj == None or db_tests_obj == []:
    pass
  else:
    first_test_exists = True
  page_dict['first_test_exists'] = first_test_exists
  # ------------------------ pull/create latest test end ------------------------
  # ------------------------ get all categories start ------------------------
  query_result_arr_of_dicts = select_general_function('select_all_employees_categories_v1')
  page_dict['all_categories_arr'] = all_employee_question_categories_sorted_function(query_result_arr_of_dicts)
  # ------------------------ get all categories end ------------------------
  if request.method == 'POST':
    # ------------------------ get ui start ------------------------
    ui_send_first_immediate = request.form.get('flexSwitchCheckDefault_01')
    ui_start_day = request.form.get('radioStartDay')
    ui_start_time = request.form.get('radioStartTime')
    ui_end_day = request.form.get('radioEndDay')
    ui_end_time = request.form.get('radioEndTime')
    ui_timezone = request.form.get('radioTimeZone')
    ui_cadence = request.form.get('radioCadence')
    ui_total_questions = request.form.get('radioTotalQuestions')
    ui_question_type = request.form.get('radioQuestionType')
    ui_select_all_categories = request.form.get('flexSwitchCheckDefault_02')
    ui_selected_categories = request.form.getlist('uiSelectedCategories')
    # ------------------------ get ui end ------------------------
    # ------------------------ check if ui is invalid start ------------------------
    if ui_start_day not in page_dict['weekdays'] or ui_end_day not in page_dict['weekdays'] or ui_start_time not in page_dict['times'] or ui_end_time not in page_dict['times'] or ui_timezone not in page_dict['timezones'] or ui_cadence not in page_dict['quiz_cadence_arr'] or int(ui_total_questions) not in page_dict['question_num_arr'] or ui_question_type not in page_dict['question_type_arr']:
      return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e6'))
    if ui_selected_categories != [] and ui_selected_categories != None:
      for i in ui_selected_categories:
        if i not in page_dict['all_categories_arr']:
          return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e6'))
    # ------------------------ check if ui is invalid start ------------------------
    # ------------------------ if settings changed start ------------------------
    settings_change_occured = False
    # ------------------------ if 'all_categories' selected start ------------------------
    if ui_select_all_categories == 'all_categories':
      if db_group_settings_dict['categories'] == 'all_categories':
        pass
      else:
        settings_change_occured = True
        db_group_settings_obj.categories = 'all_categories'
    # ------------------------ if 'all_categories' selected end ------------------------
    # ------------------------ if 'all_categories' not selected start ------------------------
    if ui_select_all_categories == None:
      if ui_selected_categories == [] or len(ui_selected_categories) == 0:
        return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e7'))
      ui_selected_categories_str = ",".join(ui_selected_categories)
      if ui_selected_categories_str == db_group_settings_dict['categories']:
        pass
      else:
        settings_change_occured = True
        db_group_settings_obj.categories = ui_selected_categories_str
    # ------------------------ if 'all_categories' not selected end ------------------------
    if ui_start_day != db_group_settings_dict['start_day']:
      settings_change_occured = True
      db_group_settings_obj.start_day = ui_start_day
    if ui_start_time != db_group_settings_dict['start_time']:
      settings_change_occured = True
      db_group_settings_obj.start_time = ui_start_time
    if ui_end_day != db_group_settings_dict['end_day']:
      settings_change_occured = True
      db_group_settings_obj.end_day = ui_end_day
    if ui_end_time != db_group_settings_dict['end_time']:
      settings_change_occured = True
      db_group_settings_obj.end_time = ui_end_time
    if ui_timezone != db_group_settings_dict['timezone']:
      settings_change_occured = True
      db_group_settings_obj.timezone = ui_timezone
    if ui_cadence != db_group_settings_dict['cadence']:
      settings_change_occured = True
      db_group_settings_obj.cadence = ui_cadence
    if int(ui_total_questions) != db_group_settings_dict['total_questions']:
      settings_change_occured = True
      db_group_settings_obj.total_questions = ui_total_questions
    if ui_question_type != db_group_settings_dict['question_type']:
      settings_change_occured = True
      db_group_settings_obj.question_type = ui_question_type
    # ------------------------ if new start/end day/times make sense start ------------------------
    start_day_index = page_dict['weekdays'].index(ui_start_day)
    start_time_index = page_dict['times'].index(ui_start_time)
    end_day_index = page_dict['weekdays'].index(ui_end_day)
    end_time_index = page_dict['times'].index(ui_end_time)
    if start_day_index > end_day_index or (start_day_index == end_day_index and start_time_index >= end_time_index):
      return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e8'))
    # ------------------------ if new start/end day/times make sense end ------------------------
    if settings_change_occured == True:
      db.session.commit()
      # ------------------------ if first quiz immediate is checked - after changes start ------------------------
      if ui_send_first_immediate == 'is_checked' and first_test_exists == False:
        create_quiz_status = create_quiz_function(page_dict['db_group_settings_dict']['fk_group_id'], True)
        if create_quiz_status == 'false_end_time':
          return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e8'))
        if create_quiz_status == True:
          return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s3'))
      # ------------------------ if first quiz immediate is checked - after changes end ------------------------
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s2'))
    # ------------------------ if settings changed end ------------------------
    # ------------------------ if first quiz immediate is checked - no changes to existing settings start ------------------------
    if ui_send_first_immediate == 'is_checked' and first_test_exists == False:
      create_quiz_status = create_quiz_function(page_dict['db_group_settings_dict']['fk_group_id'], True)
      if create_quiz_status == 'false_end_time':
        return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e8'))
      if create_quiz_status == True:
        return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s3'))
    # ------------------------ if first quiz immediate is checked - no changes to existing settings end ------------------------
    # ------------------------ if no change in settings start ------------------------
    if settings_change_occured == False:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='i1'))
    # ------------------------ if no change in settings end ------------------------
  localhost_print_function(' ------------------------ employees_schedule_function END ------------------------ ')
  return render_template('employees/interior/schedule/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/t', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_test_id_function(url_redirect_code=None, url_test_id=None, url_question_number='1'):
  localhost_print_function(' ------------------------ employees_test_id_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ redirect to latest test id start ------------------------
  user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
  if url_test_id == None:
    db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
    if db_tests_obj == None or db_tests_obj == []:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
    else:
      return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=db_tests_obj.id, url_question_number='1'))
  # ------------------------ redirect to latest test id end ------------------------
  # ------------------------ pull test id start ------------------------
  test_id = url_test_id
  db_tests_obj = EmployeesTestsObj.query.filter_by(id=test_id).first()
  if db_tests_obj == None or db_tests_obj == []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ pull test id end ------------------------
  # ------------------------ validate question number start ------------------------
  total_questions = int(db_tests_obj.total_questions)
  try:
    url_question_number = int(url_question_number)
  except:
    return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=test_id, url_question_number='1'))
  if url_question_number > total_questions or url_question_number < 1:
    return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=test_id, url_question_number='1'))
  # ------------------------ validate question number end ------------------------
  # ------------------------ pull specific question id start ------------------------
  question_ids_str = db_tests_obj.question_ids
  question_ids_arr = question_ids_str.split(',')
  desired_question_id = question_ids_arr[url_question_number-1]
  # ------------------------ pull specific question id end ------------------------
  # ------------------------ pull question from db start ------------------------
  db_question_obj = CreatedQuestionsObj.query.filter_by(id=desired_question_id).first()
  db_question_dict = arr_of_dict_all_columns_single_item_function(db_question_obj, for_json_dumps=True)
  # ------------------------ append question type start ------------------------
  question_type_order_str = db_tests_obj.question_types_order
  question_type_order_arr = question_type_order_str.split(',')
  desired_question_type = question_type_order_arr[url_question_number-1]
  db_question_dict['desired_question_type'] = desired_question_type
  # ------------------------ append question type end ------------------------
  page_dict['db_question_dict'] = db_question_dict
  # ------------------------ pull question from db end ------------------------
  # ------------------------ fix categories presentation start ------------------------
  page_dict['db_question_dict']['categories'] = categories_tuple_function(page_dict['db_question_dict']['categories'])
  # ------------------------ fix categories presentation end ------------------------
  # ------------------------ pull user info start ------------------------
  page_dict['user_company_name'] = current_user.company_name
  # ------------------------ pull user info end ------------------------
  # ------------------------ question order logic start ------------------------
  page_dict['current_question_number'] = str(int(url_question_number))
  page_dict['next_question_number'] = str(int(url_question_number) + 1)
  page_dict['previous_question_number'] = str(int(url_question_number) - 1)
  if int(db_tests_obj.total_questions) == int(url_question_number):
    page_dict['next_question_number'] = 'submit'
  # ------------------------ question order logic end ------------------------
  # ------------------------ test variables start ------------------------
  page_dict['url_test_id'] = url_test_id
  # ------------------------ test variables end ------------------------
  # ------------------------ contains image check start ------------------------
  contains_img = False
  if 'amazonaws.com' in page_dict['db_question_dict']['aws_image_url']:
    contains_img = True
  page_dict['question_contains_image'] = contains_img
  # ------------------------ contains image check end ------------------------
  # ------------------------ archive view defined start ------------------------
  page_dict['view_as_archive'] = False
  # ------------------------ archive view defined end ------------------------
  # ------------------------ redirect variables start ------------------------
  page_dict['db_question_dict']['redirect_ui_answer'] = ''
  try:
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id).first()
    db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
    master_answer_arr_of_dict = json.loads(db_test_grading_dict['test_obj'])
    for i in master_answer_arr_of_dict:
      if int(i['question_number']) == int(url_question_number):
        page_dict['db_question_dict']['redirect_ui_answer'] = i['ui_answer']
  except:
    pass
  # ------------------------ redirect variables end ------------------------
  # ------------------------ ui post start ------------------------
  if request.method == 'POST':
    # ------------------------ user input start ------------------------
    ui_answer = ''
    ui_answer_is_correct = False
    # ------------------------ user input - fill in the blank start ------------------------
    if page_dict['db_question_dict']['desired_question_type'] == 'Fill in the blank':
      ui_answer = request.form.get('ui_answer_fitb')
      # ------------------------ validate ui start ------------------------
      if len(ui_answer) < 1 or len(ui_answer) > 280:
        return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=str(url_question_number), url_redirect_code='e6'))
      # ------------------------ validate ui end ------------------------
      # ------------------------ grade ui start ------------------------
      grade_quiz_function(ui_answer, url_test_id, db_tests_obj.total_questions, url_question_number, db_question_dict, current_user.id, user_group_id.public_group_id)
      # ------------------------ grade ui end ------------------------
    # ------------------------ user input - fill in the blank end ------------------------
    # ------------------------ user input - multiple choice start ------------------------
    if page_dict['db_question_dict']['desired_question_type'] == 'Multiple choice':
      ui_answer = request.form.get('ui_answer_mcq')
      # ------------------------ validate ui start ------------------------
      allowed_answers_arr = ['a', 'b', 'c', 'd', 'e']
      if ui_answer.lower() not in allowed_answers_arr:
        return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=str(url_question_number), url_redirect_code='e6'))
      # ------------------------ validate ui start ------------------------
      # ------------------------ grade ui start ------------------------
      grade_quiz_function(ui_answer, url_test_id, db_tests_obj.total_questions, url_question_number, db_question_dict, current_user.id, user_group_id.public_group_id)
      # ------------------------ grade ui end ------------------------
    # ------------------------ user input - multiple choice end ------------------------
    # ------------------------ user input end ------------------------
    if page_dict['next_question_number'] == 'submit':
      # ------------------------ pull latest graded start ------------------------
      db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id).first()
      db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
      # ------------------------ pull latest graded end ------------------------
      if db_test_grading_dict['total_questions'] == db_test_grading_dict['graded_count']:
        return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s4'))
      else:
        unanswered_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        for i in json.loads(db_test_grading_dict['test_obj']):
          already_answered_question_number = str(i['question_number'])
          if already_answered_question_number in unanswered_arr:
            unanswered_arr.remove(already_answered_question_number)
        return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=unanswered_arr[0]))
    else:
      return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=str(int(url_question_number)+1)))
  # ------------------------ ui post end ------------------------
  localhost_print_function(' ------------------------ employees_test_id_function END ------------------------ ')
  return render_template('employees/interior/test_quiz/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------