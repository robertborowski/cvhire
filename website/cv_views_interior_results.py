# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for, make_response, send_file, Response
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import CvObj, CvInvalidFormatObj
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.cookies import redis_check_if_cookie_exists_function, browser_response_set_cookie_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import results_status_codes_function, dashboard_section_links_dict_results_function, results_table_links_function
from website.backend.db_obj_checks import get_content_function
from website.backend.uploads_user import allowed_cv_file_upload_function, get_file_suffix_function
from website.backend.read_files import get_file_contents_function
from website.backend.open_ai_chatgpt import get_name_and_email_from_cv_function
from website.backend.convert import convert_obj_row_to_dict_function
from website.backend.aws_logic import get_file_contents_from_aws_function, upload_file_to_aws_s3_function, initial_cv_scrape_function, get_file_static_from_aws_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_results = Blueprint('cv_views_interior_results', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_results.route('/results', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/', methods=['GET', 'POST'])
@login_required
def results_none_function():
  return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='all'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_results.route('/results/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def results_dashboard_general_function(url_status_code='all', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = results_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='all', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'results'
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_results_function()
  # ------------------------ get list end ------------------------
  # ------------------------ check if sort option passed start ------------------------
  sort_option_passed = None
  if url_redirect_code != None:
    if 'sort_' in url_redirect_code:
      sort_option_passed = url_redirect_code
  # ------------------------ check if sort option passed end ------------------------
  # ------------------------ get content start ------------------------
  page_dict = get_content_function(current_user, page_dict, url_status_code, page_dict['starting_route'], sort_option_passed)
  # ------------------------ get content end ------------------------
  # ------------------------ get content table links start ------------------------
  page_dict['sub_table_links_dict'] = results_table_links_function(url_status_code)
  # ------------------------ get content table links end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Results'
  page_dict['dashboard_action'] = 'Screen CV'
  page_dict['dashboard_action_link'] = '/ai/one-role-many-cvs'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'all':
    correct_template = 'interior/results/all/index.html'
  if url_status_code == 'archive':
    correct_template = 'interior/results/archived/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
