# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -note: any pages related to authentication will be in this auth.py file
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
import os
from .models import UserObj
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.sanitize import sanitize_email_function, sanitize_password_function
from website.backend.sendgrid import send_email_template_function
from website.backend.cookies import redis_check_if_cookie_exists_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_auth = Blueprint('cv_auth', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_auth.route('/signup', methods=['GET', 'POST'])
@cv_auth.route('/signup/', methods=['GET', 'POST'])
@cv_auth.route('/signup/<url_redirect_code>', methods=['GET', 'POST'])
def cv_signup_function(url_redirect_code=None):
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
    # ------------------------ post method hit #2 - full sign up start ------------------------
    ui_email = request.form.get('uiEmail')
    ui_password = request.form.get('uiPassword')
    # ------------------------ sanitize/check user inputs start ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email, 'false')
    if ui_email_cleaned == False:
      return redirect(url_for('cv_auth.cv_signup_function', url_redirect_code='e1'))
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('cv_auth.cv_signup_function', url_redirect_code='e2'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user inputs end ------------------------
    # ------------------------ check if user email already exists in db start ------------------------
    user_exists = UserObj.query.filter_by(email=ui_email).first()
    if user_exists != None and user_exists != []:
      return redirect(url_for('cv_auth.cv_signup_function', url_redirect_code='e3'))
    # ------------------------ check if user email already exists in db start ------------------------
    else:
      # ------------------------ create new user in db start ------------------------
      new_row = UserObj(
        id=create_uuid_function('user_'),
        created_timestamp=create_timestamp_function(),
        email=ui_email.lower(),
        password=generate_password_hash(ui_password, method="sha256")
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ create new user in db end ------------------------
      # ------------------------ keep user logged in start ------------------------
      login_user(new_row, remember=True)
      # ------------------------ keep user logged in end ------------------------
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('CVHIRE_NOTIFICATIONS_EMAIL')
        output_subject = f'New signup: {ui_email}'
        output_body = f'New signup: {ui_email}'
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('cv_views_interior.cv_dashboard_function'))
    # ------------------------ post method hit #2 - full sign up end ------------------------
  return render_template('exterior/signup/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_auth.route('/login', methods=['GET', 'POST'])
@cv_auth.route('/login/', methods=['GET', 'POST'])
@cv_auth.route('/login/<url_redirect_code>', methods=['GET', 'POST'])
@cv_auth.route('/login/<url_redirect_code>/', methods=['GET', 'POST'])
def cv_login_function(url_redirect_code=None):
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
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = UserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        if user != None:
          try:
            login_user(user, remember=True)
          except:
            pass
        # ------------------------ keep user logged in end ------------------------
        return redirect(url_for('cv_views_interior.cv_dashboard_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  if request.method == 'POST':
    # ------------------------ post method hit #1 - regular login start ------------------------
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('uiEmail')
    ui_password = request.form.get('uiPassword')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      return redirect(url_for('cv_auth.cv_login_function', url_redirect_code='e1'))
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('cv_auth.cv_login_function', url_redirect_code='e2'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ see if user exists start ------------------------
    user = UserObj.query.filter_by(email=ui_email).first()
    if user == None or user == []:
      return redirect(url_for('cv_auth.cv_signup_function'))
    # ------------------------ see if user exists end ------------------------
    if user:
      if check_password_hash(user.password, ui_password):
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        return redirect(url_for('cv_views_interior.cv_dashboard_function'))
      else:
        return redirect(url_for('cv_auth.cv_login_function', url_redirect_code='e4'))
    else:
      return redirect(url_for('cv_auth.cv_login_function', url_redirect_code='e4'))
    # ------------------------ post method hit #1 - regular login end ------------------------
  return render_template('exterior/login/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_auth.route('/logout')
@cv_auth.route('/logout/')
@login_required
def cv_logout_function():
  # ------------------------ loop through redis and logout all signed in cookies start ------------------------
  try:
    redis_logout_all_other_signins_function(current_user.id)
  except Exception as e:
    print(e)
    pass
  # ------------------------ loop through redis and logout all signed in cookies end ------------------------
  logout_user()
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  # ------------------------ auto sign in with cookie end ------------------------
  if get_cookie_value_from_browser != None:
    try:
      redis_connection.delete(get_cookie_value_from_browser)
    except Exception as e:
      print(e)
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  return redirect(url_for('cv_auth.cv_login_function'))
# ------------------------ individual route end ------------------------