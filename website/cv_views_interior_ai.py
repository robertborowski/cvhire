# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj, RolesObj, CvObj
import os
import json
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.cookies import redis_check_if_cookie_exists_function, browser_response_set_cookie_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import role_status_codes_function, cv_status_codes_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_ai = Blueprint('cv_views_interior_ai', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_ai.route('/home', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/home/', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/home/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_ai.route('/home/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_dashboard_function(url_redirect_code=None):
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
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