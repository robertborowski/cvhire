# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj, RolesObj, GradedObj
import os
import json
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import dashboard_section_links_dict_export_function, roles_table_links_function, export_status_codes_function
from website.backend.sanitize import sanitize_chars_function_v1, sanitize_chars_function_v2
from website.backend.db_obj_checks import get_content_function
from website.backend.convert import convert_obj_row_to_dict_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_export = Blueprint('cv_views_interior_export', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_export.route('/export', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/', methods=['GET', 'POST'])
@login_required
def cv_roles_function():
  return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_export.route('/export/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def export_dashboard_function(url_status_code='export_results', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = export_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'export'
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_export_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get total results start ------------------------
  db_grade_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').all()
  page_dict['content_total_rows'] = 0
  try:
    page_dict['content_total_rows'] = len(db_grade_obj)
  except:
    pass
  # ------------------------ get total results end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Export'
  page_dict['dashboard_action'] = 'Export results'
  page_dict['dashboard_action_link'] = '/export/export_results'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'export_results':
    correct_template = 'interior/export_pages/results/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
