# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj, RolesObj, CvObj, OpenAiQueueObj
import os
import json
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.cookies import redis_check_if_cookie_exists_function, browser_response_set_cookie_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import ai_status_codes_function, dashboard_section_links_dict_ai_function
from website.backend.db_obj_checks import get_content_split_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_ai = Blueprint('cv_views_interior_ai', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_ai.route('/ai', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/ai/', methods=['GET', 'POST'])
@login_required
def cv_none_ai_function():
  return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_ai.route('/ai/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/ai/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/ai/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/ai/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_dashboard_function(url_status_code='one-role-many-cvs', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = ai_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'ai'
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_ai_function()
  # ------------------------ get list end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Artificial Intelligence'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ get content start ------------------------
  page_dict = get_content_split_function(current_user, page_dict, 'roles')
  page_dict = get_content_split_function(current_user, page_dict, 'cv')
  # ------------------------ get content end ------------------------
  # ------------------------ for setting cookie start ------------------------
  correct_template = ''
  if url_status_code == 'one-role-many-cvs':
    correct_template = 'interior/ai/one-role-many-cvs/index.html'
  if url_status_code == 'one-cv-many-roles':
    correct_template = 'interior/ai/one-cv-many-roles/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_one_role_selected = request.form.get('radio-one-role')
    ui_many_cv_selected = request.form.getlist('checkbox-many-cvs')
    ui_many_roles_selected = request.form.getlist('checkbox-many-roles')
    ui_one_cv_selected = request.form.get('radio-one-cv')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ only two allowed inputs start ------------------------
    bad_inputs = False
    if (ui_one_role_selected == None and ui_many_cv_selected != []) or (ui_one_cv_selected == None and ui_many_roles_selected != []):
      bad_inputs = True
    if (ui_one_role_selected != None and ui_many_cv_selected == []) or (ui_one_cv_selected != None and ui_many_roles_selected == []):
      bad_inputs = True
    if bad_inputs == True:
      return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e10'))
    # ------------------------ only two allowed inputs end ------------------------
    # ------------------------ set variables start ------------------------
    question_type = 'one-role-many-cvs'
    if ui_one_role_selected == None:
      question_type = 'one-cv-many-roles'
    single_value = ''
    multiple_arr = []
    multiple_value = ''
    # ------------------------ set variables end ------------------------
    # ------------------------ get from db start ------------------------
    # ------------------------ question type 1 start ------------------------
    if question_type == 'one-role-many-cvs':
      # ------------------------ single start ------------------------
      db_role_obj = RolesObj.query.filter_by(id=ui_one_role_selected).first()
      if db_role_obj == None:
        return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e10'))
      single_value = ui_one_role_selected
      # ------------------------ single end ------------------------
      # ------------------------ multiple start ------------------------
      for i in ui_many_cv_selected:
        db_cv_obj = CvObj.query.filter_by(id=i).first()
        multiple_arr.append(db_cv_obj.id)
      if len(multiple_arr) == 0:
        return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e10'))
      multiple_value = ','.join(multiple_arr)
      if len(multiple_value) > 2000:
        return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e13'))
      # ------------------------ multiple end ------------------------
    # ------------------------ question type 1 end ------------------------
    # ------------------------ question type 2 start ------------------------
    if question_type == 'one-cv-many-roles':
      # ------------------------ single start ------------------------
      db_cv_obj = CvObj.query.filter_by(id=ui_one_cv_selected).first()
      if db_cv_obj == None:
        return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e10'))
      single_value = ui_one_cv_selected
      # ------------------------ single end ------------------------
      # ------------------------ multiple start ------------------------
      for i in ui_many_roles_selected:
        db_role_obj = RolesObj.query.filter_by(id=i).first()
        multiple_arr.append(db_role_obj.id)
      if len(multiple_arr) == 0:
        return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e10'))
      multiple_value = ','.join(multiple_arr)
      if len(multiple_value) > 2000:
        return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e13'))
      # ------------------------ multiple end ------------------------
    # ------------------------ question type 2 end ------------------------
    # ------------------------ get from db end ------------------------
    # ------------------------ add to queue start ------------------------
    new_row = OpenAiQueueObj(
      id = create_uuid_function('queue_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      status = 'requested',
      question_type = question_type,
      single_value = single_value,
      multiple_values = multiple_value
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ add to queue end ------------------------
    # ------------------------ trigger queue start ------------------------
    # ------------------------ trigger queue end ------------------------
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='i3'))
  # ------------------------ post end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(correct_template, user=current_user, page_dict_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function(current_user, correct_template, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------