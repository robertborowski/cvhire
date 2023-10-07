# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for, make_response, send_file, Response
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import CvObj, CvInvalidFormatObj
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import cv_status_codes_function, dashboard_section_links_dict_cv_function, cv_table_links_function
from website.backend.db_obj_checks import get_content_function
from website.backend.uploads_user import allowed_cv_file_upload_function, get_file_suffix_function
from website.backend.aws_logic import upload_file_to_aws_s3_function, initial_cv_scrape_function, get_file_static_from_aws_function
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
  page_dict['starting_route'] = 'cv'
  page_dict['nav_header'] = True
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_cv_function()
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
  page_dict['sub_table_links_dict'] = cv_table_links_function(url_status_code)
  # ------------------------ get content table links end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'CVs & Resumes'
  page_dict['dashboard_action'] = 'Add CV'
  page_dict['dashboard_action_link'] = '/cv/add'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ autofill newly added cv/resumes start ------------------------
  updates_occurred = initial_cv_scrape_function(current_user.id)
  if updates_occurred == True:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code=url_redirect_code))
  # ------------------------ autofill newly added cv/resumes end ------------------------
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
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ if no files uploaded start ------------------------
    if 'uiFormFileMultipleUpload' not in request.files:
      return redirect(url_for('cv_views_interior_cv.cv_add_function', url_redirect_code='e10'))
    # ------------------------ if no files uploaded end ------------------------
    # ------------------------ get user inputs start ------------------------
    files_uploaded_arr = request.files.getlist('uiFormFileMultipleUpload')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ loop through each file start ------------------------
    for i_file in files_uploaded_arr:
      try:
        # ------------------------ check file name empty start ------------------------
        if i_file.filename == '':
          return redirect(url_for('cv_views_interior_cv.cv_add_function', url_redirect_code='e11'))
        # ------------------------ check file name empty end ------------------------
        # ------------------------ check valid file format start ------------------------
        valid_format = allowed_cv_file_upload_function(i_file.filename)
        # ------------------------ check valid file format end ------------------------
        # ------------------------ if file format is not valid start ------------------------
        if valid_format == False:
          file_format_suffix = get_file_suffix_function(i_file.filename)
          # ------------------------ upload to db start ------------------------
          new_row = CvInvalidFormatObj(
            id=create_uuid_function('cv_fail_'),
            created_timestamp=create_timestamp_function(),
            fk_user_id=current_user.id,
            invalid_file_type=file_format_suffix
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ upload to db end ------------------------
        # ------------------------ if file format is not valid end ------------------------
        # ------------------------ look and upload start ------------------------
        if i_file and valid_format == True:
          try:
            # ------------------------ set variables start ------------------------
            file_format_suffix = get_file_suffix_function(i_file.filename)
            cv_aws_id = create_uuid_function('cv_aws_')
            aws_file_name = cv_aws_id + file_format_suffix
            # ------------------------ set variables end ------------------------
            # ------------------------ upload to aws s3 start ------------------------
            upload_file_to_aws_s3_function(i_file, aws_file_name)
            # ------------------------ upload to aws s3 end ------------------------
            # ------------------------ upload to db start ------------------------
            new_row = CvObj(
              id=create_uuid_function('cv_'),
              created_timestamp=create_timestamp_function(),
              fk_user_id=current_user.id,
              status='active',
              cv_upload_name=i_file.filename,
              cv_aws_id=aws_file_name,
              candidate_email=None,
              candidate_name=None,
              candidate_phone=None,
              initial_scrape_complete=False
            )
            db.session.add(new_row)
            db.session.commit()
            # ------------------------ upload to db end ------------------------
          except Exception as e:
            pass
        else:
          continue
        # ------------------------ look and upload end ------------------------
      except Exception as e:
        continue
    # ------------------------ loop through each file end ------------------------
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='s7'))
  # ------------------------ post end ------------------------
  return render_template('interior/cv/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_cv.route('/cv/view/<url_cv_id>')
@cv_views_interior_cv.route('/cv/view/<url_cv_id>/')
@login_required
def cv_view_function(url_cv_id=None):
  # ------------------------ if no id given start ------------------------
  if url_cv_id == None:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active'))
  # ------------------------ if no id given end ------------------------
  # ------------------------ check if id exists and is assigned to user start ------------------------
  db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,id=url_cv_id).first()
  if db_obj == None:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active'))
  # ------------------------ check if id exists and is assigned to user end ------------------------
  # ------------------------ get file suffix start ------------------------
  file_format_suffix = get_file_suffix_function(db_obj.cv_aws_id)
  # ------------------------ get file suffix end ------------------------
  try:
    # ------------------------ file type start ------------------------
    if file_format_suffix == '.pdf':
      response = get_file_static_from_aws_function(db_obj.cv_aws_id)
      return Response(response, content_type='application/pdf')
    # ------------------------ file type end ------------------------
    # ------------------------ file type start ------------------------
    elif file_format_suffix == '.docx' or file_format_suffix == '.txt':
      response = get_file_static_from_aws_function(db_obj.cv_aws_id)
      output = Response(response)
      output.headers["Content-Disposition"] = f"attachment; filename={db_obj.cv_upload_name}"
      if file_format_suffix == '.docx':
        output.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # MIME type for .docx
      elif file_format_suffix == '.txt':
        output.headers["Content-Type"] = "text/plain"  # MIME type for .txt
      return output
    # ------------------------ file type end ------------------------
  except Exception as e:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='e12'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_cv.route('/cv/ask_ai/<url_item_id>', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/ask_ai/<url_item_id>/', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/ask_ai/<url_item_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_cv.route('/cv/ask_ai/<url_item_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def results_ask_function(url_item_id=None, url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ route incorrect check start ------------------------
  if url_item_id == None:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_redirect_code='e10'))
  # ------------------------ route incorrect check end ------------------------
  # ------------------------ set variables start ------------------------
  db_obj = None
  # ------------------------ set variables end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = False
  page_dict['view_reason'] = 'ask_cv'
  # ------------------------ set variables end ------------------------
  # ------------------------ get from db start ------------------------
  db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,id=url_item_id).filter(CvObj.status!='delete').first()
  if db_obj == None or db_obj == []:
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_redirect_code='e10'))
  # ------------------------ get from db end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    pass
  # ------------------------ post end ------------------------
  return render_template('interior/cv/ask_ai/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------