# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserAttributesObj
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import dashboard_section_links_dict_account_function, roles_table_links_function, account_status_codes_function
from website.backend.sanitize import sanitize_chars_function_v1, sanitize_chars_function_v2
from website.backend.db_obj_checks import get_user_content_function
from website.backend.convert import convert_obj_row_to_dict_function
from website.backend.sanitize import sanitize_fullname_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_account = Blueprint('cv_views_interior_account', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/', methods=['GET', 'POST'])
@login_required
def cv_account_function():
  return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/settings', methods=['GET', 'POST'])
@cv_views_interior_account.route('/settings/', methods=['GET', 'POST'])
@login_required
def cv_settings_function():
  return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_account_dashboard_function(url_status_code='user', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = account_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'account'
  page_dict['nav_header'] = True
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_account_function()
  # ------------------------ get list end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Account'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ section start ------------------------
  # ------------------------ get content start ------------------------
  page_dict = get_user_content_function(current_user, page_dict, url_status_code, page_dict['starting_route'])
  # ------------------------ get content end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['current_user_email'] = current_user.email
  if url_status_code == 'user':
    page_dict['view_reason'] = 'edit_account'
  if url_status_code == 'settings':
    page_dict['view_reason'] = 'edit_settings'
  # ------------------------ set variables end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    if url_status_code == 'user':
      # ------------------------ get user inputs start ------------------------
      ui_full_name = request.form.get('uiFullName')
      ui_company_name = request.form.get('uiCompanyName')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize user inputs start ------------------------
      ui_full_name_check = sanitize_fullname_function(ui_full_name)
      ui_company_name_check = sanitize_fullname_function(ui_company_name)
      # ------------------------ sanitize user inputs end ------------------------
      # ------------------------ redirect error start ------------------------
      if ui_full_name_check == False or ui_company_name_check == False:
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e8'))
      # ------------------------ redirect error end ------------------------
      # ------------------------ update db start ------------------------
      change_occurred = False
      # ------------------------ full name start ------------------------
      db_full_name_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='full_name').first()
      if db_full_name_obj.attribute_value != ui_full_name:
        db_full_name_obj.attribute_value = ui_full_name
        change_occurred = True
      # ------------------------ full name end ------------------------
      # ------------------------ company name start ------------------------
      db_company_name_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='company_name').first()
      if db_company_name_obj.attribute_value != ui_company_name:
        db_company_name_obj.attribute_value = ui_company_name
        change_occurred = True
      # ------------------------ company name end ------------------------
      if change_occurred == True:
        db.session.commit()
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='s5'))
      # ------------------------ update db end ------------------------
  # ------------------------ post end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'user':
    correct_template = 'interior/account/user/index.html'
  if url_status_code == 'settings':
    correct_template = 'interior/account/settings_acc/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account/verify/email/send', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/verify/email/send/', methods=['GET', 'POST'])
@login_required
def account_verify_send_function():
  # ------------------------ set variables start ------------------------
  verification_code = ''
  # ------------------------ set variables end ------------------------
  # ------------------------ check if verify code exists start ------------------------
  db_verify_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='verification_email_code').first()
  # ------------------------ check if verify code exists end ------------------------
  # ------------------------ if verify code does not exist start ------------------------
  if db_verify_obj == None or db_verify_obj == []:
    verification_code = create_uuid_function('verify_')
    # ------------------------ new row start ------------------------
    new_row = UserAttributesObj(
      id=create_uuid_function('attribute_'),
      created_timestamp=create_timestamp_function(),
      fk_user_id=current_user.id,
      attribute_key='verification_email_code',
      attribute_value=verification_code
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ new row end ------------------------
  # ------------------------ if verify code does not exist end ------------------------
  # ------------------------ if verify code does exist start ------------------------
  else:
    verification_code = db_verify_obj.attribute_value
  # ------------------------ if verify code does exist end ------------------------
  # ------------------------ send email to user start ------------------------
  # ------------------------ send email to user end ------------------------
  return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='s3'))
# ------------------------ individual route end ------------------------
