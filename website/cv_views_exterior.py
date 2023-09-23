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
def cv_landing_details_function(url_reference_id=None):
  # ------------------------ ref id hit start ------------------------
  if url_reference_id != None:
    return redirect(url_for('cv_auth.cv_signup_function'))
  # ------------------------ ref id hit end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict = {}
  # ------------------------ set variables end ------------------------
  return render_template('exterior/landing/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/reset', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<url_redirect_code>', methods=['GET', 'POST'])
def cv_forgot_password_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  forgot_password_error_statement = ''
  if request.method == 'POST':
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('forgot_password_page_ui_email')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      forgot_password_error_statement = 'Please enter a valid work email.'
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ check if user email exists in db start ------------------------
    user_exists = UserObj.query.filter_by(email=ui_email,signup_product='polling').first()
    if user_exists:
      forgot_password_error_statement = 'Password reset link sent to email.'
      # ------------------------ send email with token url start ------------------------
      serializer_token_obj = UserObj.get_reset_token_function(self=user_exists)
      output_email = ui_email
      output_subject_line = 'Password Reset - HerdReviews'
      output_message_content = f"To reset your password, visit the following link: https://herdreviews.com/reset/{serializer_token_obj}/ \
                                This link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
    # ------------------------ success code start ------------------------
    alert_message_dict = alert_message_default_function_v2('s13')
    page_dict['alert_message_dict'] = alert_message_dict
    # ------------------------ success code end ------------------------
  return render_template('polling/exterior/forgot_password/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/reset/<token>', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<token>/', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<token>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_exterior.route('/reset/<token>/<url_redirect_code>/', methods=['GET', 'POST'])
def cv_reset_forgot_password_function(token, url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  user_obj_from_token = UserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    return redirect(url_for('cv_views_exterior.cv_reset_forgot_password_function', token=token, url_redirect_code='e28'))
  if request.method == 'POST':
    # ------------------------ get inputs from form start ------------------------
    ui_password = request.form.get('reset_forgot_password_page_ui_password')
    ui_password_confirmed = request.form.get('reset_forgot_password_page_ui_password_confirmed')
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
  return render_template('polling/exterior/forgot_password/reset_forgot_password/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

"""
# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/blog')
@cv_views_exterior.route('/blog/')
def cv_all_blogs_function():
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  # ------------------------ get all blogs start ------------------------
  master_arr_of_dicts = []
  blog_obj = BlogPollingObj.query.filter_by(status=True).order_by(BlogPollingObj.created_timestamp.desc()).all()
  for i_obj in blog_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    i_dict['title_url'] = i_dict['title'].replace(' ','-')
    i_dict['title'] = i_dict['title'][:50] + '...'
    i_dict['details'] = i_dict['details'][:100] + '...'
    master_arr_of_dicts.append(i_dict)
  page_dict['master_arr_of_dicts'] = master_arr_of_dicts
  # ------------------------ get all blogs end ------------------------
  return render_template('polling/exterior/blog/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/blog/<i_blog_post_title>')
@cv_views_exterior.route('/blog/<i_blog_post_title>/')
def cv_i_blog_page_function(i_blog_post_title=None):
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  if i_blog_post_title == None or i_blog_post_title == '':
    return redirect(url_for('cv_views_exterior.cv_all_blogs_function'))
  try:
    # ------------------------ replace hyphen start ------------------------
    i_blog_post_title = i_blog_post_title.replace('-',' ')
    # ------------------------ replace hyphen end ------------------------
    blog_obj = BlogPollingObj.query.filter_by(title=i_blog_post_title).first()
    if blog_obj == None or blog_obj == '':
      return redirect(url_for('cv_views_exterior.cv_all_blogs_function'))
    else:
      page_dict['blog_dict'] = arr_of_dict_all_columns_single_item_function(blog_obj)
      page_dict['blog_dict']['created_timestamp_date'] = page_dict['blog_dict']['created_timestamp'].date()
  except:
    return redirect(url_for('cv_views_exterior.cv_all_blogs_function'))
  current_blog_post_num_full_string = f'polling/exterior/blog/blogs_by_id/{blog_obj.id}.html'
  return render_template(current_blog_post_num_full_string, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
"""

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/privacy')
@cv_views_exterior.route('/privacy/')
def cv_privacy_function():
  return render_template('polling/exterior/privacy/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/terms')
@cv_views_exterior.route('/terms/')
def cv_terms_function():
  return render_template('polling/exterior/tos/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/about')
@cv_views_exterior.route('/about/')
def cv_about_function():
  return render_template('polling/exterior/about/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/faq')
@cv_views_exterior.route('/faq/')
def cv_faq_function():
  return render_template('polling/exterior/faq/index.html')
# ------------------------ individual route end ------------------------