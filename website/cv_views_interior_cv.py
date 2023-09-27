# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj, RolesObj
import os
import json
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.cookies import redis_check_if_cookie_exists_function, browser_response_set_cookie_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import cv_status_codes_function, dashboard_section_links_dict_cv_function, cv_table_links_function
from website.backend.db_obj_checks import get_content_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_cv = Blueprint('cv_views_interior_cv', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_cv.route('/cv', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/', methods=['GET', 'POST'])
@login_required
def cv_none_function():
  return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_cv.route('/cv/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_dashboard_general_function(url_status_code='active', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = cv_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_cv_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_content_function(current_user, page_dict, url_status_code, 'cv')
  # ------------------------ get roles end ------------------------
  # ------------------------ get role table links start ------------------------
  page_dict['roles_table_links_dict'] = cv_table_links_function(url_status_code)
  # ------------------------ get role table links end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'CVs & Resumes'
  page_dict['dashboard_action'] = 'Add CV'
  page_dict['dashboard_action_link'] = '/cv/add'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'active':
    correct_template = 'interior/cv/active/index.html'
  if url_status_code == 'archive':
    correct_template = 'interior/cv/archive_cv/index.html'
  if url_status_code == 'all':
    correct_template = 'interior/cv/all_cv/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_cv.route('/cv/add', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/add/', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/add/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/add/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_add_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/cv/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
