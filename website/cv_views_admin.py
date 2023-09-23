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
from website.models import UserObj
import os
from datetime import datetime
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.sanitize import sanitize_email_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_admin = Blueprint('cv_views_admin', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_admin.route('/admin', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_function(url_redirect_code=None):
  # ------------------------ check admin status start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('cv_views_interior.cv_dashboard_function'))
  # ------------------------ check admin status end ------------------------
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
    if user_exists and user_exists.email != os.environ.get('RUN_TEST_EMAIL'):
      # ------------------------ lock user start ------------------------
      user_exists.locked=True
      db.session.commit()
      return redirect(url_for('cv_views_admin.admin_function', url_redirect_code='s1'))
      # ------------------------ lock user end ------------------------
    else:
      pass
    # ------------------------ check if user email exists in db end ------------------------
    # ------------------------ success code start ------------------------
    alert_message_dict = get_alert_message_function('i1')
    page_dict['alert_message_dict'] = alert_message_dict
    # ------------------------ success code end ------------------------
  print(' ------------- 100-admin start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    print(f"k: {k} | v: {v}")
    pass
  print(' ------------- 100-admin end ------------- ')
  return render_template('interior/admin_templates/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
