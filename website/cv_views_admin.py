# ------------------------ imports start ------------------------
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailBlockObj
import os
from datetime import datetime
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.sanitize import sanitize_email_function
from website.backend.static_lists import get_list_function, redis_all_keys_function
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
    return redirect(url_for('cv_views_interior.cv_dashboard_function', url_redirect_code='e5'))
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
    # ------------------------ post #1 start ------------------------
    ui_email = request.form.get('uiEmail')
    if ui_email != None:
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
    # ------------------------ post #1 end ------------------------
    # ------------------------ post #2 start ------------------------
    ui_block_email_like = request.form.get('uiBlockEmailLike')
    if ui_block_email_like != None:
      blocked_email_arr = get_list_function('blocked_email_arr')
      if ui_block_email_like not in blocked_email_arr:
        # ------------------------ create new user in db start ------------------------
        try:
          new_row = EmailBlockObj(
            id=ui_block_email_like,
            created_timestamp=create_timestamp_function()
          )
          db.session.add(new_row)
          db.session.commit()
          return redirect(url_for('cv_views_admin.admin_function', url_redirect_code='s2'))
        except:
          return redirect(url_for('cv_views_admin.admin_function', url_redirect_code='e7'))
        # ------------------------ create new user in db end ------------------------
      else:
        return redirect(url_for('cv_views_admin.admin_function', url_redirect_code='i2'))
    # ------------------------ post #2 end ------------------------
    # ------------------------ post #3 start ------------------------
    ui_redis_clear_all = request.form.get('uiRedisClearAll')
    if ui_redis_clear_all != None:
      redis_all_keys = redis_all_keys_function()
      # ------------------------ loop through keys start ------------------------
      for key in redis_all_keys:
        redis_value = redis_connection.get(key).decode('utf-8')
        if 'bcooke' in key.decode('utf-8'):
          pass
          # print(f"key: {key} | redis_value: {redis_value}")
          # redis_connection.delete(key.decode('utf-8'))
      # ------------------------ loop through keys end ------------------------
    # ------------------------ post #3 end ------------------------
  return render_template('interior/admin_templates/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
