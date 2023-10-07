# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for, make_response, send_file, Response
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import GradedObj, OpenAiQueueObj, CvObj
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import results_status_codes_function, dashboard_section_links_dict_results_function, results_table_links_function, get_stars_img_function
from website.backend.db_obj_checks import get_content_function
from website.backend.convert import convert_obj_row_to_dict_function, get_follow_ups_function
from website.backend.db_manipulation import additional_cv_info_from_db_function
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
  return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='valid'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_results.route('/results/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def results_dashboard_general_function(url_status_code='valid', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = results_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='valid', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'results'
  page_dict['nav_header'] = True
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
  # ------------------------ check if any grading is currently in progress start ------------------------
  page_dict['queue_status'] = False
  db_queue_obj = OpenAiQueueObj.query.filter_by(fk_user_id=current_user.id,status='requested').all()
  if db_queue_obj != None and db_queue_obj != []:
    page_dict['queue_status'] = True
  # ------------------------ check if any grading is currently in progress end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'valid':
    correct_template = 'interior/results/valid/index.html'
  if url_status_code == 'archive':
    correct_template = 'interior/results/archived/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_results.route('/results/view/<url_grade_id>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/view/<url_grade_id>/', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/view/<url_grade_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/view/<url_grade_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def results_view_function(url_grade_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if no role id given start ------------------------
  if url_grade_id == None:
    return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='valid'))
  # ------------------------ if no role id given end ------------------------
  # ------------------------ check if role id exists and is assigned to user start ------------------------
  db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id,id=url_grade_id).first()
  if db_obj == None:
    return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='valid'))
  page_dict['db_grade_dict'] = convert_obj_row_to_dict_function(db_obj)
  # ------------------------ check if role id exists and is assigned to user end ------------------------
  # ------------------------ star images start ------------------------
  page_dict['db_grade_dict'] = get_stars_img_function(page_dict['db_grade_dict'])
  # ------------------------ star images end ------------------------
  # ------------------------ follow ups start ------------------------
  page_dict['db_grade_dict']['follow_ups_arr'] = get_follow_ups_function(page_dict['db_grade_dict'])
  # ------------------------ follow ups end ------------------------
  # ------------------------ get additional CV info start ------------------------
  page_dict['db_grade_dict'] = additional_cv_info_from_db_function(current_user.id, page_dict['db_grade_dict'])
  # ------------------------ get additional CV info end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['view_reason'] = 'view_result'
  # ------------------------ set variables end ------------------------
  return render_template('interior/results/view_results/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_results.route('/results/ask/<url_starting_route_id>/<url_item_id>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/ask/<url_starting_route_id>/<url_item_id>/', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/ask/<url_starting_route_id>/<url_item_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_results.route('/results/ask/<url_starting_route_id>/<url_item_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def results_ask_function(url_starting_route_id=None, url_item_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ route incorrect check start ------------------------
  if url_starting_route_id == None or url_item_id == None:
    return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='valid'))
  # ------------------------ route incorrect check end ------------------------
  # ------------------------ set variables start ------------------------
  db_obj = None
  page_dict['view_reason'] = None
  # ------------------------ set variables end ------------------------
  # ------------------------ starting route start ------------------------
  if url_starting_route_id == 'cv':
    # ------------------------ set variables start ------------------------
    page_dict['view_reason'] = 'ask_cv'
    # ------------------------ set variables end ------------------------
    # ------------------------ get from db start ------------------------
    db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,id=url_item_id).filter(CvObj.status!='delete').first()
    if db_obj == None or db_obj == []:
      return redirect(url_for('cv_views_interior_results.results_dashboard_general_function', url_status_code='valid',url_redirect_code='e10'))
    # ------------------------ get from db end ------------------------
    # ------------------------ post start ------------------------
    if request.method == 'POST':
      pass
    # ------------------------ post end ------------------------
  # ------------------------ starting route end ------------------------
  return render_template('interior/results/ask/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
