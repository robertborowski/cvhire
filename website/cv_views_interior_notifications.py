# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import RolesObj, GradedObj
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import dashboard_section_links_dict_notifications_function, notifications_table_links_function, notifications_status_codes_function
from website.backend.sanitize import sanitize_chars_function_v1, sanitize_chars_function_v2
from website.backend.db_obj_checks import get_content_function
from website.backend.convert import convert_obj_row_to_dict_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_notifications = Blueprint('cv_views_interior_notifications', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_notifications.route('/notifications', methods=['GET', 'POST'])
@cv_views_interior_notifications.route('/notifications/', methods=['GET', 'POST'])
@login_required
def cv_notifications_function():
  return redirect(url_for('cv_views_interior_notifications.cv_notifications_dashboard_function', url_status_code='unread'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_notifications.route('/notifications/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_notifications.route('/notifications/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_notifications.route('/notifications/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_notifications.route('/notifications/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_notifications_dashboard_function(url_status_code='unread', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if not verified start ------------------------
  if page_dict['verified_email'] == False:
    return redirect(url_for('cv_views_interior_account.force_verify_page_function'))
  # ------------------------ if not verified end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = notifications_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_notifications.cv_notifications_dashboard_function', url_status_code='unread', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'notifications'
  page_dict['nav_header'] = True
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_notifications_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_content_function(current_user, page_dict, url_status_code, page_dict['starting_route'])
  # ------------------------ get roles end ------------------------
  # ------------------------ get role table links start ------------------------
  page_dict['sub_table_links_dict'] = notifications_table_links_function(url_status_code)
  # ------------------------ get role table links end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Notifications'
  page_dict['dashboard_action'] = 'no action'
  page_dict['dashboard_action_link'] = 'no action'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'unread':
    correct_template = 'interior/notifications/unread/index.html'
  if url_status_code == 'read':
    correct_template = 'interior/notifications/read/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
