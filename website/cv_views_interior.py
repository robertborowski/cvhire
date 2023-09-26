# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

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
from website.backend.static_lists import roles_links_function, roles_table_links_function
from website.backend.sanitize import sanitize_chars_function_v1, sanitize_chars_function_v2
from website.backend.db_obj_checks import get_roles_function
from website.backend.convert import convert_obj_row_to_dict_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior = Blueprint('cv_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/home', methods=['GET', 'POST'])
@cv_views_interior.route('/home/', methods=['GET', 'POST'])
@cv_views_interior.route('/home/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/home/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_dashboard_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, page_dict_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/locked', methods=['GET', 'POST'])
@cv_views_interior.route('/locked/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/locked/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_locked_function(url_redirect_code=None):
  # ------------------------ locked status start ------------------------
  if current_user.locked != True:
    return redirect(url_for('cv_views_interior.cv_dashboard_function'))
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
@cv_views_interior.route('/cv', methods=['GET', 'POST'])
@cv_views_interior.route('/cv/', methods=['GET', 'POST'])
@cv_views_interior.route('/cv/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/cv/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_resume_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/cv/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_function(url_redirect_code=None):
  return redirect(url_for('cv_views_interior.cv_roles_open_function', url_redirect_code=url_redirect_code))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles/open', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/open/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/open/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/open/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_open_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['role_link_dict'] = roles_links_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_roles_function(current_user, page_dict, 'open')
  # ------------------------ get roles end ------------------------
  # ------------------------ get role table links start ------------------------
  page_dict['roles_table_links_dict'] = roles_table_links_function('open')
  # ------------------------ get role table links end ------------------------
  return render_template('interior/roles/open/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles/filled', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/filled/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/filled/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/filled/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_filled_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['role_link_dict'] = roles_links_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_roles_function(current_user, page_dict, 'filled')
  # ------------------------ get roles end ------------------------
  return render_template('interior/roles/filled/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles/archive', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/archive/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/archive/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/archive/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_archive_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['role_link_dict'] = roles_links_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_roles_function(current_user, page_dict, 'archive')
  # ------------------------ get roles end ------------------------
  return render_template('interior/roles/archive_role/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles/all', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/all/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/all/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/all/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_all_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['role_link_dict'] = roles_links_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_roles_function(current_user, page_dict, 'all')
  # ------------------------ get roles end ------------------------
  return render_template('interior/roles/all_role/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles/add', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/add/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/add/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/add/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_add_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ for later edits start ------------------------
  page_dict['db_role_dict'] = None
  # ------------------------ for later edits end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ user inputs start ------------------------
    ui_role_name = request.form.get('uiRoleName')
    ui_about = request.form.get('uiAbout')
    ui_requirements = request.form.get('uiRequirements')
    ui_nice_to_haves = request.form.get('uiNiceToHaves')
    # ------------------------ user inputs end ------------------------
    # ------------------------ sanitize user inputs error start ------------------------
    ui_role_name_check = sanitize_chars_function_v2(ui_role_name)
    ui_about_check = sanitize_chars_function_v1(ui_about)
    ui_requirements_check = sanitize_chars_function_v1(ui_requirements)
    ui_nice_to_haves_check = sanitize_chars_function_v1(ui_nice_to_haves)
    if ui_role_name_check == False or ui_about_check == False or ui_requirements_check == False or ui_nice_to_haves_check == False:
      return redirect(url_for('cv_views_interior.cv_roles_add_function', url_redirect_code='e8'))
    # ------------------------ sanitize user inputs error end ------------------------
    # ------------------------ check if role exists start ------------------------
    db_obj = RolesObj.query.filter_by(name=ui_role_name,fk_user_id=current_user.id).first()
    if db_obj != None and db_obj != []:
      return redirect(url_for('cv_views_interior.cv_roles_add_function', url_redirect_code='e9'))
    # ------------------------ check if role exists end ------------------------
    # ------------------------ new row start ------------------------
    try:
      new_row = RolesObj(
        id=create_uuid_function('role_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        status='open',
        name=ui_role_name,
        about=ui_about,
        requirements=ui_requirements,
        nice_to_haves=ui_nice_to_haves
      )
      db.session.add(new_row)
      db.session.commit()
      return redirect(url_for('cv_views_interior.cv_roles_open_function', url_redirect_code='s4'))
    except:
      pass
    # ------------------------ new row end ------------------------
  # ------------------------ post end ------------------------
  return render_template('interior/roles/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/roles/edit', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/edit/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/edit/<url_role_id>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/edit/<url_role_id>/', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/edit/<url_role_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/roles/edit/<url_role_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_edit_function(url_role_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if no role id given start ------------------------
  if url_role_id == None:
    return redirect(url_for('cv_views_interior.cv_roles_open_function'))
  # ------------------------ if no role id given end ------------------------
  # ------------------------ check if role id exists and is assigned to user start ------------------------
  db_role_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,id=url_role_id).first()
  page_dict['db_role_dict'] = convert_obj_row_to_dict_function(db_role_obj)
  # ------------------------ check if role id exists and is assigned to user end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ user inputs start ------------------------
    ui_role_name = request.form.get('uiRoleName')
    ui_about = request.form.get('uiAbout')
    ui_requirements = request.form.get('uiRequirements')
    ui_nice_to_haves = request.form.get('uiNiceToHaves')
    # ------------------------ user inputs end ------------------------
    # ------------------------ sanitize user inputs error start ------------------------
    ui_role_name_check = sanitize_chars_function_v2(ui_role_name)
    ui_about_check = sanitize_chars_function_v1(ui_about)
    ui_requirements_check = sanitize_chars_function_v1(ui_requirements)
    ui_nice_to_haves_check = sanitize_chars_function_v1(ui_nice_to_haves)
    if ui_role_name_check == False or ui_about_check == False or ui_requirements_check == False or ui_nice_to_haves_check == False:
      return redirect(url_for('cv_views_interior.cv_roles_edit_function', url_role_id=url_role_id, url_redirect_code='e8'))
    # ------------------------ sanitize user inputs error end ------------------------
    change_occured = False
    # ------------------------ check if chenges occured start ------------------------
    if db_role_obj.name != ui_role_name:
      # ------------------------ check if role exists start ------------------------
      db_role_name_check_obj = RolesObj.query.filter_by(name=ui_role_name,fk_user_id=current_user.id).first()
      if db_role_name_check_obj != None and db_role_name_check_obj != []:
        return redirect(url_for('cv_views_interior.cv_roles_edit_function', url_role_id=url_role_id, url_redirect_code='e9'))
      else:
        db_role_obj.name = ui_role_name
        change_occured = True
      # ------------------------ check if role exists end ------------------------
    if db_role_obj.about != ui_about:
      db_role_obj.about = ui_about
      change_occured = True
    if db_role_obj.requirements != ui_requirements:
      db_role_obj.requirements = ui_requirements
      change_occured = True
    if db_role_obj.nice_to_haves != ui_nice_to_haves:
      db_role_obj.nice_to_haves = ui_nice_to_haves
      change_occured = True
    if change_occured == True:
      db.session.commit()
      return redirect(url_for('cv_views_interior.cv_roles_open_function', url_redirect_code='s5'))
    if change_occured == False:
      return redirect(url_for('cv_views_interior.cv_roles_open_function', url_redirect_code='i1'))
    # ------------------------ check if chenges occured end ------------------------
  # ------------------------ post end ------------------------
  return render_template('interior/roles/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/favorites', methods=['GET', 'POST'])
@cv_views_interior.route('/favorites/', methods=['GET', 'POST'])
@cv_views_interior.route('/favorites/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/favorites/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_favorites_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  return render_template('interior/favorites/index.html', page_dict_html=page_dict)
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