# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj
import os
import json
from datetime import datetime
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.user_attributes_check import onboarding_checks_function
from website.backend.cookies import redis_check_if_cookie_exists_function, browser_response_set_cookie_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior = Blueprint('cv_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/dashboard', methods=['GET', 'POST'])
@cv_views_interior.route('/dashboard/', methods=['GET', 'POST'])
@cv_views_interior.route('/dashboard/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/dashboard/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_dashboard_function(url_redirect_code=None):
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
  # ------------------------ locked status start ------------------------
  if current_user.locked == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ locked status end ------------------------
  """
  # ------------------------ onboarding checks start ------------------------
  onbaording_status = onboarding_checks_function(current_user)
  if onbaording_status == 'verify':
    page_dict['verified_email_status'] = False
  if onbaording_status != None:
    return redirect(url_for('cv_views_interior.cv_feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  """
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  print(' ------------- 100-dashboard start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    print(f"k: {k} | v: {v}")
    pass
  print(' ------------- 100-dashboard end ------------- ')
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, page_dict_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior.route('/locked', methods=['GET', 'POST'])
@cv_views_interior.route('/locked/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior.route('/locked/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_locked_function(url_redirect_code=None):
  # ------------------------ locked status start ------------------------
  if current_user.locked != True:
    return redirect(url_for('cv_views_interior.cv_dashboard_function'))
  # ------------------------ locked status end ------------------------
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
  return render_template('interior/locked/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
