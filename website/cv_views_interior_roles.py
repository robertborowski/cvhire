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
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import roles_links_function, roles_table_links_function, role_status_codes_function
from website.backend.sanitize import sanitize_chars_function_v1, sanitize_chars_function_v2
from website.backend.db_obj_checks import get_roles_function
from website.backend.convert import convert_obj_row_to_dict_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_roles = Blueprint('cv_views_interior_roles', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_roles.route('/roles', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/', methods=['GET', 'POST'])
@login_required
def cv_roles_function():
  return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_roles.route('/roles/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_dashboard_function(url_status_code='open', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  role_status_codes_arr = role_status_codes_function()
  if url_status_code not in role_status_codes_arr:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['role_link_dict'] = roles_links_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get roles start ------------------------
  page_dict = get_roles_function(current_user, page_dict, url_status_code)
  # ------------------------ get roles end ------------------------
  # ------------------------ get role table links start ------------------------
  page_dict['roles_table_links_dict'] = roles_table_links_function(url_status_code)
  # ------------------------ get role table links end ------------------------
  print(' ------------- 100 start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    print(f"k: {k} | v: {v}")
    pass
  print(' ------------- 100 end ------------- ')
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'open':
    correct_template = 'interior/roles/open/index.html'
  if url_status_code == 'filled':
    correct_template = 'interior/roles/filled/index.html'
  if url_status_code == 'archive':
    correct_template = 'interior/roles/archive_role/index.html'
  if url_status_code == 'all':
    correct_template = 'interior/roles/all_role/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_roles.route('/roles/add', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/add/', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/add/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/add/<url_redirect_code>/', methods=['GET', 'POST'])
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
      return redirect(url_for('cv_views_interior_roles.cv_roles_add_function', url_redirect_code='e8'))
    # ------------------------ sanitize user inputs error end ------------------------
    # ------------------------ check if role exists start ------------------------
    db_obj = RolesObj.query.filter_by(name=ui_role_name,fk_user_id=current_user.id).first()
    if db_obj != None and db_obj != []:
      return redirect(url_for('cv_views_interior_roles.cv_roles_add_function', url_redirect_code='e9'))
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
      return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='s4'))
    except:
      pass
    # ------------------------ new row end ------------------------
  # ------------------------ post end ------------------------
  return render_template('interior/roles/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_roles.route('/roles/edit', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/edit/', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/edit/<url_role_id>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/edit/<url_role_id>/', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/edit/<url_role_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/edit/<url_role_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_edit_function(url_role_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if no role id given start ------------------------
  if url_role_id == None:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open'))
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
      return redirect(url_for('cv_views_interior_roles.cv_roles_edit_function', url_role_id=url_role_id, url_redirect_code='e8'))
    # ------------------------ sanitize user inputs error end ------------------------
    change_occured = False
    # ------------------------ check if chenges occured start ------------------------
    if db_role_obj.name != ui_role_name:
      # ------------------------ check if role exists start ------------------------
      db_role_name_check_obj = RolesObj.query.filter_by(name=ui_role_name,fk_user_id=current_user.id).first()
      if db_role_name_check_obj != None and db_role_name_check_obj != []:
        return redirect(url_for('cv_views_interior_roles.cv_roles_edit_function', url_role_id=url_role_id, url_redirect_code='e9'))
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
      return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='s5'))
    if change_occured == False:
      return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='i1'))
    # ------------------------ check if chenges occured end ------------------------
  # ------------------------ post end ------------------------
  return render_template('interior/roles/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_roles.route('/roles/view/<url_role_id>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/view/<url_role_id>/', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/view/<url_role_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/view/<url_role_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_view_function(url_role_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if no role id given start ------------------------
  if url_role_id == None:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open',))
  # ------------------------ if no role id given end ------------------------
  # ------------------------ check if role id exists and is assigned to user start ------------------------
  db_role_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,id=url_role_id).first()
  if db_role_obj == None:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open',))
  page_dict['db_role_dict'] = convert_obj_row_to_dict_function(db_role_obj)
  # ------------------------ check if role id exists and is assigned to user end ------------------------
  return render_template('interior/roles/view_role/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_roles.route('/roles/status/<url_status_code>/<url_role_id>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/status/<url_status_code>/<url_role_id>/', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/status/<url_status_code>/<url_role_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_roles.route('/roles/status/<url_status_code>/<url_role_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_roles_status_change_function(url_status_code=None, url_role_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if none start ------------------------
  if url_status_code == None or url_role_id == None:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='e10'))
  # ------------------------ if none end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  role_status_codes_arr = role_status_codes_function()
  if url_status_code not in role_status_codes_arr:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ check if role id is valid for user start ------------------------
  db_role_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,id=url_role_id).first()
  if db_role_obj == None:
    return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='e10'))
  # ------------------------ check if role id is valid for user end ------------------------
  # ------------------------ change status start ------------------------
  if db_role_obj.status != url_status_code:
    db_role_obj.status = url_status_code
    db.session.commit()
    if url_status_code == 'delete':
      return redirect(url_for(f'cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='s6'))
    return redirect(url_for(f'cv_views_interior_roles.cv_roles_dashboard_function', url_status_code=url_status_code, url_redirect_code='s5'))
  # ------------------------ change status end ------------------------
  return redirect(url_for('cv_views_interior_roles.cv_roles_dashboard_function', url_status_code='open', url_redirect_code='i1'))
# ------------------------ individual route end ------------------------
