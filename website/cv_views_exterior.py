# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.backend.connection import redis_connect_open_function
from website.models import UserObj, EmailSentObj, EmailScrapedObj, BlogObj
from website import db
from werkzeug.security import generate_password_hash
from website.backend.alerts import get_alert_message_function
from website.backend.sanitize import sanitize_email_function, sanitize_password_function
from website.backend.sendgrid import send_email_template_function
import os
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.convert import objs_to_arr_of_dicts_function
from website.backend.static_lists import get_blog_posts_function, navbar_link_dict_exterior_function, faq_dict_exterior_function
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
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  # ------------------------ get faq variables start ------------------------
  page_dict['faq_dict'] = faq_dict_exterior_function()
  # ------------------------ get faq variables end ------------------------
  # ------------------------ ref id hit start ------------------------
  if url_reference_id != None:
    return redirect(url_for('cv_auth.cv_signup_function'))
  # ------------------------ ref id hit end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = True
  page_dict['is_blog_page'] = False
  # ------------------------ set variables end ------------------------
  # ------------------------ get latest blog post start ------------------------
  db_blog_objs = get_blog_posts_function()
  # ------------------------ get latest blog post end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_blog_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ post #1 start ------------------------
    # ------------------------ get ui start ------------------------
    ui_email_footer = request.form.get('uiEmailFooter')
    # ------------------------ get ui end ------------------------
    if ui_email_footer != None and ui_email_footer != '':
      return redirect(url_for('cv_views_exterior.email_signup_checker_function', url_redirect_code=ui_email_footer))
    # ------------------------ post #1 end ------------------------
    # ------------------------ post #2 start ------------------------
    # ------------------------ get ui start ------------------------
    ui_email = request.form.get('uiEmail')
    # ------------------------ get ui end ------------------------
    if ui_email != None and ui_email != '':
      return redirect(url_for('cv_views_exterior.email_signup_checker_function', url_redirect_code=ui_email))
    # ------------------------ post #2 end ------------------------
  # ------------------------ post end ------------------------
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
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = False
  # ------------------------ set variables end ------------------------
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
      # ------------------------ add to email sent table start ------------------------
      try:
        new_row = EmailSentObj(
          id=create_uuid_function('sent_'),
          created_timestamp=create_timestamp_function(),
          from_user_id_fk='standard',
          to_email=ui_email,
          subject=output_subject_line,
          body='forgot password reset link'
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ add to email sent table end ------------------------
      # ------------------------ email self notifications start ------------------------
      try:
        output_to_email = os.environ.get('CVHIRE_NOTIFICATIONS_EMAIL')
        output_subject = f'{ui_email} | {output_subject_line}'
        output_body = f'{ui_email} | {output_subject_line}'
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self notifications end ------------------------
    else:
      pass
    # ------------------------ check if user email exists in db end ------------------------
    # ------------------------ success code start ------------------------
    alert_message_dict = get_alert_message_function('s3')
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
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = False
  # ------------------------ set variables end ------------------------
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

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/privacy', methods=['GET', 'POST'])
@cv_views_exterior.route('/privacy/', methods=['GET', 'POST'])
def cv_privacy_function():
  page_dict = {}
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = True
  page_dict['is_blog_page'] = False
  # ------------------------ set variables end ------------------------
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  # ------------------------ get faq variables start ------------------------
  page_dict['faq_dict'] = faq_dict_exterior_function()
  # ------------------------ get faq variables end ------------------------
  # ------------------------ get latest blog post start ------------------------
  db_blog_objs = get_blog_posts_function()
  # ------------------------ get latest blog post end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_blog_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ post #1 start ------------------------
    # ------------------------ get ui start ------------------------
    ui_email_footer = request.form.get('uiEmailFooter')
    # ------------------------ get ui end ------------------------
    if ui_email_footer != None and ui_email_footer != '':
      return redirect(url_for('cv_views_exterior.email_signup_checker_function', url_redirect_code=ui_email_footer))
    # ------------------------ post #1 end ------------------------
  # ------------------------ post end ------------------------
  return render_template('exterior/privacy_terms/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/email/unsubscribe')
@cv_views_exterior.route('/email/unsubscribe/')
@cv_views_exterior.route('/email/unsubscribe/<url_id_code>')
@cv_views_exterior.route('/email/unsubscribe/<url_id_code>/')
def email_unsubscribe_function(url_id_code=None):
  page_dict = {}
  page_dict['nav_header'] = False
  # ------------------------ if url code is none start ------------------------
  if url_id_code == None:
    return redirect(url_for('cv_views_exterior.cv_landing_details_function'))
  # ------------------------ if url code is none end ------------------------
  # ------------------------ check if url id exists start ------------------------
  db_email_obj = EmailScrapedObj.query.filter_by(id=url_id_code).first()
  if db_email_obj == None or db_email_obj == []:
    return redirect(url_for('cv_views_exterior.cv_landing_details_function'))
  # ------------------------ check if url id exists end ------------------------
  # ------------------------ update db start ------------------------
  if db_email_obj.unsubscribed == False:
    db_email_obj.unsubscribed = True
    db.session.commit()
  # ------------------------ update db end ------------------------
  return render_template('exterior/unsubscribed/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/feature/<url_feature_code>', methods=['GET', 'POST'])
@cv_views_exterior.route('/feature/<url_feature_code>/', methods=['GET', 'POST'])
def feature_pages_function(url_feature_code=None):
  # ------------------------ get feature code start ------------------------
  if url_feature_code == None:
    url_feature_code = 'one-role-many-cvs'
  # ------------------------ get feature code end ------------------------
  page_dict = {}
  page_dict['nav_header'] = True
  page_dict['is_blog_page'] = False
  page_dict['url_feature_code'] = url_feature_code
  # ------------------------ get latest blog post start ------------------------
  db_blog_objs = get_blog_posts_function()
  # ------------------------ get latest blog post end ------------------------
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  # ------------------------ get faq variables start ------------------------
  page_dict['faq_dict'] = faq_dict_exterior_function()
  # ------------------------ get faq variables end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_blog_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ post #1 start ------------------------
    # ------------------------ get ui start ------------------------
    ui_email_footer = request.form.get('uiEmailFooter')
    # ------------------------ get ui end ------------------------
    if ui_email_footer != None and ui_email_footer != '':
      return redirect(url_for('cv_views_exterior.email_signup_checker_function', url_redirect_code=ui_email_footer))
    # ------------------------ post #1 end ------------------------
  # ------------------------ post end ------------------------
  return render_template('exterior/features/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/pricing', methods=['GET', 'POST'])
@cv_views_exterior.route('/pricing/', methods=['GET', 'POST'])
def pricing_function(url_feature_code=None):
  # ------------------------ set variables start ------------------------
  page_dict = {}
  page_dict['nav_header'] = True
  page_dict['is_blog_page'] = False
  page_dict['url_feature_code'] = url_feature_code
  # ------------------------ set variables end ------------------------
  # ------------------------ get latest blog post start ------------------------
  db_blog_objs = get_blog_posts_function()
  # ------------------------ get latest blog post end ------------------------
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  # ------------------------ get faq variables start ------------------------
  page_dict['faq_dict'] = faq_dict_exterior_function()
  # ------------------------ get faq variables end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_blog_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ post #1 start ------------------------
    # ------------------------ get ui start ------------------------
    ui_email_footer = request.form.get('uiEmailFooter')
    # ------------------------ get ui end ------------------------
    if ui_email_footer != None and ui_email_footer != '':
      return redirect(url_for('cv_views_exterior.email_signup_checker_function', url_redirect_code=ui_email_footer))
    # ------------------------ post #1 end ------------------------
  # ------------------------ post end ------------------------
  return render_template('exterior/pricing/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_exterior.route('/email/check')
@cv_views_exterior.route('/email/check/')
@cv_views_exterior.route('/email/check/<url_redirect_code>')
@cv_views_exterior.route('/email/check/<url_redirect_code>/')
def email_signup_checker_function(url_redirect_code=None):
  # ------------------------ if none provided start ------------------------
  if url_redirect_code == None or url_redirect_code == '':
    return redirect(url_for('cv_views_exterior.cv_landing_details_function'))
  # ------------------------ if none provided end ------------------------
  # ------------------------ set variable start ------------------------
  ui_email = url_redirect_code
  # ------------------------ set variable end ------------------------
  # ------------------------ sanitize/check user input email start ------------------------
  ui_email_cleaned = sanitize_email_function(ui_email, 'true')
  if ui_email_cleaned == False:
    return redirect(url_for('cv_auth.cv_signup_function', url_redirect_code='e1'))
  # ------------------------ sanitize/check user input email end ------------------------
  # ------------------------ redirect to login start ------------------------
  user_exists = UserObj.query.filter_by(email=ui_email).first()
  if user_exists != None and user_exists != []:
    return redirect(url_for('cv_auth.cv_login_function', url_redirect_code=ui_email))
  # ------------------------ redirect to login end ------------------------
  # ------------------------ redirect to signup start ------------------------
  return redirect(url_for('cv_auth.cv_signup_function', url_redirect_code=ui_email))
  # ------------------------ redirect to signup end ------------------------
# ------------------------ individual route end ------------------------