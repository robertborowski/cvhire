# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import FeedbackObj
import os
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import dashboard_section_links_dict_help_function, help_status_codes_function
from website.backend.sanitize import sanitize_chars_function_v3
from website.backend.sendgrid import send_email_template_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_help = Blueprint('cv_views_interior_help', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_help.route('/help', methods=['GET', 'POST'])
@cv_views_interior_help.route('/help/', methods=['GET', 'POST'])
@login_required
def cv_help_function():
  return redirect(url_for('cv_views_interior_help.help_dashboard_function', url_status_code='request'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_help.route('/help/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_help.route('/help/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_help.route('/help/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_help.route('/help/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def help_dashboard_function(url_status_code='request', url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = help_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_help.help_dashboard_function', url_status_code='request', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'help'
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_help_function()
  # ------------------------ get list end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Help center'
  page_dict['dashboard_action'] = 'Request feature'
  page_dict['dashboard_action_link'] = '/help/request'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'request':
    correct_template = 'interior/help/request/index.html'
  # ------------------------ choose correct template end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    try:
      # ------------------------ get user inputs start ------------------------
      ui_feedback = request.form.get('uiFeedback')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize user inputs start ------------------------
      ui_feedback_check = sanitize_chars_function_v3(ui_feedback)
      if ui_feedback_check == False:
        return redirect(url_for('cv_views_interior_help.help_dashboard_function', url_redirect_code='e8'))
      # ------------------------ sanitize user inputs end ------------------------
      # ------------------------ insert to db start ------------------------
      try:
        new_row = FeedbackObj(
          id=create_uuid_function('feedback_'),
          created_timestamp=create_timestamp_function(),
          fk_user_id=current_user.id,
          status='open',
          message=ui_feedback
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ insert to db end ------------------------
      # ------------------------ set variables start ------------------------
      output_subject = f'{current_user.email} | Help center'
      output_body = f'{current_user.email}: {ui_feedback}'
      # ------------------------ set variables end ------------------------
      # ------------------------ email self support start ------------------------
      try:
        output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self support end ------------------------
      # ------------------------ email self notifications start ------------------------
      try:
        output_to_email = os.environ.get('CVHIRE_NOTIFICATIONS_EMAIL')
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self notifications end ------------------------
    except Exception as e:
      print(f'Error help_dashboard_function: {e}')
      return redirect(url_for('cv_views_interior_help.help_dashboard_function', url_status_code='request', url_redirect_code='s10'))
    return redirect(url_for('cv_views_interior_help.help_dashboard_function', url_status_code='request', url_redirect_code='s9'))
  # ------------------------ post end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
