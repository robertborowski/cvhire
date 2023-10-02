# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj, RolesObj, CvObj
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
    # ------------------------ get user inputs end ------------------------
    print(' ------------- 0 ------------- ')
    print(f"ui_one_role_selected | type: {type(ui_one_role_selected)} | {ui_one_role_selected}")
    print(f"ui_many_cv_selected | type: {type(ui_many_cv_selected)} | {ui_many_cv_selected}")
    print(' ------------- 0 ------------- ')
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs'))
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