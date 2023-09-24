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
from flask_login import current_user
from website.backend.connection import redis_connect_open_function
from website.models import UserObj
from website import db
from werkzeug.security import generate_password_hash
from website.backend.alerts import get_alert_message_function
from website.backend.sanitize import sanitize_email_function, sanitize_password_function
from website.backend.sendgrid import send_email_template_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_exterior = Blueprint('cv_views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/', methods=['GET', 'POST'])
@cv_views_exterior.route('/<url_reference_id>', methods=['GET', 'POST'])
@cv_views_exterior.route('/<url_reference_id>/', methods=['GET', 'POST'])
@cv_views_exterior.route('/<url_reference_id>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_exterior.route('/<url_reference_id>/<url_redirect_code>/', methods=['GET', 'POST'])
def cv_landing_details_function(url_reference_id=None, url_redirect_code=None):
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
  # ------------------------ ref id hit start ------------------------
  if url_reference_id != None:
    return redirect(url_for('cv_auth.cv_signup_function'))
  # ------------------------ ref id hit end ------------------------
  return render_template('exterior/landing/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/reset', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<url_redirect_code>', methods=['GET', 'POST'])
def cv_forgot_password_function(url_redirect_code=None):
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
  if request.method == 'POST':
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('uiEmail')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      pass
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ check if user email exists in db start ------------------------
    user_exists = UserObj.query.filter_by(email=ui_email,locked=False).first()
    if user_exists:
      # ------------------------ send email with token url start ------------------------
      serializer_token_obj = UserObj.get_reset_token_function(self=user_exists)
      output_email = ui_email
      output_subject_line = 'Password Reset | CVhire'
      output_message_content = f"To reset your password, visit the following link: http://127.0.0.1/reset/{serializer_token_obj}/ \
                                This link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      pass
    # ------------------------ check if user email exists in db end ------------------------
    # ------------------------ success code start ------------------------
    alert_message_dict = get_alert_message_function('s13')
    page_dict['alert_message_dict'] = alert_message_dict
    # ------------------------ success code end ------------------------
  return render_template('exterior/reset/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/reset/<token>', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<token>/', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<token>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<token>/<url_redirect_code>/', methods=['GET', 'POST'])
def cv_reset_forgot_password_function(token, url_redirect_code=None):
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
  user_obj_from_token = UserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    return redirect(url_for('cv_views_exterior.cv_reset_forgot_password_function', token=token, url_redirect_code='e28'))
  if request.method == 'POST':
    # ------------------------ get inputs from form start ------------------------
    ui_password = request.form.get('uiPassword1')
    ui_password_confirmed = request.form.get('uiPassword2')
    # ------------------------ get inputs from form end ------------------------
    # ------------------------ check match start ------------------------
    if ui_password != ui_password_confirmed:
      return redirect(url_for('cv_views_exterior.cv_reset_forgot_password_function', token=token, url_redirect_code='e29'))
    # ------------------------ check match end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('cv_views_exterior.cv_reset_forgot_password_function', token=token, url_redirect_code='e6'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_confirmed_cleaned = sanitize_password_function(ui_password_confirmed)
    if ui_password_confirmed_cleaned == False:
      return redirect(url_for('cv_views_exterior.cv_reset_forgot_password_function', token=token, url_redirect_code='e6'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ update db start ------------------------
    user_obj_from_token.password = generate_password_hash(ui_password, method="sha256")
    db.session.commit()
    return redirect(url_for('cv_auth.cv_login_function', url_redirect_code='s6'))
    # ------------------------ update db end ------------------------
  return render_template('exterior/reset/reset_confirm/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------