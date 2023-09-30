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
from website.backend.static_lists import role_status_codes_function, cv_status_codes_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior = Blueprint('cv_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/locked', methods=['GET', 'POST'])
@cv_views_interior.route('/locked/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/locked/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_locked_function(url_redirect_code=None):
  # ------------------------ locked status start ------------------------
  if current_user.locked != True:
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function'))
  # ------------------------ locked status end ------------------------
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = get_alert_message_function(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  return render_template('interior/locked/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/account', methods=['GET', 'POST'])
@cv_views_interior.route('/account/', methods=['GET', 'POST'])
@cv_views_interior.route('/account/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/account/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_account_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/account/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/help', methods=['GET', 'POST'])
@cv_views_interior.route('/help/', methods=['GET', 'POST'])
@cv_views_interior.route('/help/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/help/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_help_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/help/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/notifications', methods=['GET', 'POST'])
@cv_views_interior.route('/notifications/', methods=['GET', 'POST'])
@cv_views_interior.route('/notifications/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/notifications/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_notifications_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/notifications/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/settings', methods=['GET', 'POST'])
@cv_views_interior.route('/settings/', methods=['GET', 'POST'])
@cv_views_interior.route('/settings/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/settings/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_settings_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/settings_user/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/results', methods=['GET', 'POST'])
@cv_views_interior.route('/results/', methods=['GET', 'POST'])
@cv_views_interior.route('/results/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/results/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_favorites_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/results/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/export', methods=['GET', 'POST'])
@cv_views_interior.route('/export/', methods=['GET', 'POST'])
@cv_views_interior.route('/export/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/export/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_export_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/export_user/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/<url_section_code>/status/<url_status_code>/<url_db_item_id>', methods=['GET', 'POST'])
@cv_views_interior.route('/<url_section_code>/status/<url_status_code>/<url_db_item_id>/', methods=['GET', 'POST'])
@cv_views_interior.route('/<url_section_code>/status/<url_status_code>/<url_db_item_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/<url_section_code>/status/<url_status_code>/<url_db_item_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_general_status_change_function(url_section_code=None, url_status_code=None, url_db_item_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if none start ------------------------
  if url_section_code == None or url_status_code == None or url_db_item_id == None:
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_redirect_code='e10'))
  # ------------------------ if none end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  if url_section_code == 'roles':
    status_codes_arr = role_status_codes_function()
    if url_status_code not in status_codes_arr:
      return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='e10'))
  if url_section_code == 'cv':
    status_codes_arr = cv_status_codes_function()
    if url_status_code not in status_codes_arr:
      return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ check if role id is valid for user start ------------------------
  if url_section_code == 'roles':
    db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,id=url_db_item_id).first()
    if db_obj == None:
      return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='e10'))
  if url_section_code == 'cv':
    db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,id=url_db_item_id).first()
    if db_obj == None:
      return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='e10'))
  # ------------------------ check if role id is valid for user end ------------------------
  # ------------------------ change status start ------------------------
  if db_obj.status != url_status_code:
    db_obj.status = url_status_code
    db.session.commit()
    if url_status_code == 'delete':
      if url_section_code == 'roles':
        return redirect(url_for(f'cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='s6'))
      if url_section_code == 'cv':
        return redirect(url_for(f'cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='s6'))
    if url_section_code == 'roles':
      return redirect(url_for(f'cv_views_interior_roles.cv_roles_dashboard_function', url_status_code=url_status_code, url_redirect_code='s5'))
    if url_section_code == 'cv':
      return redirect(url_for(f'cv_views_interior_cv.cv_dashboard_general_function', url_status_code=url_status_code, url_redirect_code='s5'))
  # ------------------------ change status end ------------------------
  if url_section_code == 'roles':
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='i1'))
  if url_section_code == 'cv':
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='i1'))
# ------------------------ individual route end ------------------------