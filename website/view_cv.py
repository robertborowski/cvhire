# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for, make_response, send_file, Response
from flask_login import login_required, current_user, logout_user
from website import db
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.user_create import create_user_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
view_cv = Blueprint('view_cv', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@view_cv.route('/v2/cv/add', methods=['GET', 'POST'])
@view_cv.route('/v2/cv/add/', methods=['GET', 'POST'])
@view_cv.route('/v2/cv/add/<url_redirect_code>', methods=['GET', 'POST'])
@view_cv.route('/v2/cv/add/<url_redirect_code>/', methods=['GET', 'POST'])
# @login_required
def cv_add_function(url_redirect_code=None):
  # ------------------------ if user anonymous start ------------------------
  try:
    if current_user.email:
      pass
  except Exception as e:
    create_user_function(None, None, None)
  # ------------------------ if user anonymous end ------------------------
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if not verified start ------------------------
  if page_dict['verified_email'] == False:
    return redirect(url_for('cv_views_interior_account.force_verify_page_function'))
  # ------------------------ if not verified end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = False
  page_dict['view_reason'] = 'add_cv'
  # ------------------------ set variables end ------------------------
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
        # ------------------------ non subscriber limit check start ------------------------
        if page_dict['subscribe_status'] != 'active':
          limit_reached = non_subscriber_limit_add_cv_function(current_user)
          if limit_reached == True:
            return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='e15'))
        # ------------------------ non subscriber limit check end ------------------------
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
    # ------------------------ email self notifications start ------------------------
    try:
      output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
      output_subject = f'New CV(s) added'
      output_body = f'email: {current_user.email}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self notifications end ------------------------
    return redirect(url_for('cv_views_interior_cv.cv_dashboard_general_function', url_status_code='active', url_redirect_code='s7'))
  # ------------------------ post end ------------------------
  return render_template('interior/cv/add/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
