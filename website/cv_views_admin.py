# ------------------------ imports start ------------------------
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserObj, EmailBlockObj, EmailScrapedObj, CompanyInfoObj, EmailSentObj, BlogObj
import os
from website.backend.connection import redis_connect_open_function
from website.backend.alerts import get_alert_message_function
from website.backend.sanitize import sanitize_email_function
from website.backend.static_lists import get_list_function, redis_all_keys_function
from website.backend.selenium_script import linkedin_scraper_function
from website.backend.db_manipulation import form_scraped_emails_function, delete_from_scraped_emails_function
from datetime import datetime
from website.backend.sendgrid import send_email_template_function
from website.backend.sql_queries import update_query_v2_function, update_query_v3_function
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
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
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e5'))
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
  return render_template('interior/admin_templates/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_admin.route('/admin/control', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/control/', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/control/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/control/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def admin_control_function(url_redirect_code=None):
  # ------------------------ check admin status start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e5'))
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
          print(f"key: {key} | redis_value: {redis_value}")
          redis_connection.delete(key.decode('utf-8'))
      # ------------------------ loop through keys end ------------------------
    # ------------------------ post #3 end ------------------------
  return render_template('interior/admin_templates/control/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_admin.route('/admin/scrape', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/scrape/', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/scrape/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/scrape/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def admin_scrape_function(url_redirect_code=None):
  # ------------------------ check admin status start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e5'))
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
  # ------------------------ get latest company name start ------------------------
  db_obj = CompanyInfoObj.query.order_by(CompanyInfoObj.created_timestamp.desc()).first()
  page_dict['latest_company_url'] = db_obj.url
  # ------------------------ get latest company name end ------------------------
  if request.method == 'POST':
    # ------------------------ post #5 start ------------------------
    ui_run_script_call = request.form.get('uiRunScriptLinkedIn')
    if ui_run_script_call != None:
      # ------------------------ selenium script start ------------------------
      linkedin_scraper_function()
      # ------------------------ selenium script end ------------------------
      return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s13'))
    # ------------------------ post #5 end ------------------------
    # ------------------------ post #6 start ------------------------
    ui_company_name = request.form.get('uiCompanyName')
    ui_company_url = request.form.get('uiCompanyUrl')
    if ui_company_name != None and ui_company_url != None:
      # ------------------------ update all previous companies to false start ------------------------
      # ------------------------ open db connection start ------------------------
      postgres_connection, postgres_cursor = postgres_connect_open_function()
      # ------------------------ open db connection end ------------------------
      # ------------------------ update db start ------------------------
      try:
        update_query_v3_function(postgres_connection, postgres_cursor)
      except Exception as e:
        print(f'Exception admin_scrape_function: {e}')
        pass
      # ------------------------ update db end ------------------------
      # ------------------------ close db connection start ------------------------
      postgres_connect_close_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
      # ------------------------ update all previous companies to false end ------------------------
      db_obj = CompanyInfoObj.query.filter_by(name=ui_company_name.lower()).first()
      if db_obj == None or db_obj == []:
        # ------------------------ add to db start ------------------------
        try:
          new_row = CompanyInfoObj(
            id=create_uuid_function('company_'),
            created_timestamp=create_timestamp_function(),
            name=ui_company_name.lower(),
            url=ui_company_url.lower(),
            active=True
          )
          db.session.add(new_row)
          db.session.commit()
        except:
          pass
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s12'))
        # ------------------------ add to db end ------------------------
      else:
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='e10'))
    # ------------------------ post #6 end ------------------------
    # ------------------------ post #7 start ------------------------
    ui_form_scraped_emails = request.form.get('uiFormScrapedEmails')
    if ui_form_scraped_emails != None:
      form_scraped_emails_function()
      return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s12'))
    # ------------------------ post #7 end ------------------------
    # ------------------------ post #8 start ------------------------
    ui_delete_incorrect_scraped_emails = request.form.get('uiDeleteIncorrectScrapedEmails')
    if ui_delete_incorrect_scraped_emails != None:
      delete_from_scraped_emails_function()
      return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s12'))
    # ------------------------ post #8 end ------------------------
    # ------------------------ post #9 start ------------------------
    ui_company_url_to_update = request.form.get('uiCompanyUrlToUpdate')
    ui_int_to_update = request.form.get('uiIntToUpdate')
    if ui_company_url_to_update != None and ui_int_to_update != None:
      # ------------------------ sanitize/check inputs start ------------------------
      db_obj = CompanyInfoObj.query.filter_by(url=ui_company_url_to_update).first()
      if db_obj == None or db_obj == []:
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='e10'))
      try:
        ui_int_to_update = int(ui_int_to_update)
      except:
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='e10'))
      # ------------------------ sanitize/check inputs end ------------------------
      # ------------------------ open db connection start ------------------------
      postgres_connection, postgres_cursor = postgres_connect_open_function()
      # ------------------------ open db connection end ------------------------
      # ------------------------ update db start ------------------------
      try:
        update_query_v2_function(postgres_connection, postgres_cursor, ui_int_to_update, ui_company_url_to_update)
      except Exception as e:
        print(f'Exception admin_scrape_function: {e}')
        pass
      # ------------------------ update db end ------------------------
      # ------------------------ close db connection start ------------------------
      postgres_connect_close_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
      return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s12'))
    # ------------------------ post #9 end ------------------------
    # ------------------------ post #10 start ------------------------
    ui_print_emails = request.form.get('uiPrintEmails')
    if ui_print_emails != None:
      # ------------------------ get all emails start ------------------------
      db_email_objs = EmailScrapedObj.query.filter(EmailScrapedObj.unsubscribed == False,EmailScrapedObj.correct_format != None,EmailScrapedObj.verified == False).order_by(EmailScrapedObj.website_address.asc(),EmailScrapedObj.all_formats.asc()).all()
      # ------------------------ get all emails end ------------------------
      # ------------------------ loop emails start ------------------------
      for i_email_obj in db_email_objs:
        # ------------------------ get to email start ------------------------
        email_formats_arr = i_email_obj.all_formats.split('~')
        output_to_email = email_formats_arr[i_email_obj.correct_format] + '@' + i_email_obj.website_address
        # ------------------------ get to email end ------------------------
        print(output_to_email)
      # ------------------------ loop emails end ------------------------
      return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s12'))
    # ------------------------ post #10 end ------------------------
    # ------------------------ post #11 start ------------------------
    ui_company_url_guess = request.form.get('uiCompanyUrlGuess')
    ui_employee_name_like = request.form.get('uiEmployeeName')
    if ui_company_url_guess != None and ui_employee_name_like != None:
      db_obj_all = EmailScrapedObj.query.filter_by(website_address=ui_company_url_guess).filter(EmailScrapedObj.all_formats.like(f'%{ui_employee_name_like}%')).all()
      # ------------------------ print person 1 start ------------------------
      db_obj = db_obj_all[0]
      # ------------------------ if not found start ------------------------
      if db_obj == None or db_obj == []:
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='e10'))
      # ------------------------ if not found end ------------------------
      arr = db_obj.all_formats.split('~')
      print(' ---------- person 1 ---------- ')
      for i in arr:
        email = i + '@' + db_obj.website_address
        print(email)
      print(' ')
      # ------------------------ print person 1 end ------------------------
      """
      # ------------------------ print person 2 start ------------------------
      db_obj = db_obj_all[1]
      # ------------------------ if not found start ------------------------
      if db_obj == None or db_obj == []:
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='e10'))
      # ------------------------ if not found end ------------------------
      arr = db_obj.all_formats.split('~')
      print(' ---------- person 2 ---------- ')
      for i in arr:
        email = i + '@' + db_obj.website_address
        print(email)
      print(' ')
      # ------------------------ print person 2 end ------------------------
      # ------------------------ print person 3 start ------------------------
      db_obj = db_obj_all[2]
      # ------------------------ if not found start ------------------------
      if db_obj == None or db_obj == []:
        return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='e10'))
      # ------------------------ if not found end ------------------------
      arr = db_obj.all_formats.split('~')
      print(' ---------- person 3 ---------- ')
      for i in arr:
        email = i + '@' + db_obj.website_address
        print(email)
      print(' ')
      # ------------------------ print person 3 end ------------------------
      """
      return redirect(url_for('cv_views_admin.admin_scrape_function', url_redirect_code='s12'))
    # ------------------------ post #11 end ------------------------
  return render_template('interior/admin_templates/scrape/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_admin.route('/admin/email', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/email/', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/email/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_admin.route('/admin/email/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def admin_email_function(url_redirect_code=None):
  # ------------------------ check admin status start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e5'))
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
    ui_send_marketing_email = request.form.get('uiSendMarketingEmail')
    if ui_send_marketing_email != None:
      # ------------------------ get latest blog post info start ------------------------
      db_blog_objs = BlogObj.query.filter_by(status=True).order_by(BlogObj.created_timestamp.desc()).limit(5).all()
      # ------------------------ get latest blog post info end ------------------------
      # ------------------------ set variables start ------------------------
      today = datetime.today()
      today_format = today.strftime('%m/%d/%Y')
      output_subject = f'Resume Scanning with AI | {today_format}'
      # ------------------------ set variables end ------------------------
      # ------------------------ get all emails start ------------------------
      db_email_objs = EmailScrapedObj.query.filter(EmailScrapedObj.unsubscribed == False,EmailScrapedObj.correct_format != None,EmailScrapedObj.verified == True).order_by(EmailScrapedObj.website_address.asc(),EmailScrapedObj.all_formats.asc()).all()
      # ------------------------ get all emails end ------------------------
      # ------------------------ loop emails start ------------------------
      for i_email_obj in db_email_objs:
        # ------------------------ set variables start ------------------------
        output_body = f"""<p>Hi there,</p>\
                          <p>Resume scanning with AI tool <a href="https://cvhire.com/">CVhire</a>. Work smarter with AI and get promoted. Checkout our latest blog posts:</p>\
                          <ul>\
                          <li>Blog post: <a href="https://cvhire.com/blog/{db_blog_objs[0].slug}">{db_blog_objs[0].title}</a></li>\
                          <li>Blog post: <a href="https://cvhire.com/blog/{db_blog_objs[1].slug}">{db_blog_objs[1].title}</a></li>\
                          </ul>\
                          <p style='margin:0;'>Best,</p>\
                          <p style='margin:0;'>CVhire Support Team</p>\
                          <p style='margin:0;font-size:10px;margin-top:5px;'><a href="https://cvhire.com/email/unsubscribe/{i_email_obj.id}">unsubscribe</a></p>"""
        # ------------------------ set variables end ------------------------
        # ------------------------ get to email start ------------------------
        email_formats_arr = i_email_obj.all_formats.split('~')
        output_to_email = email_formats_arr[i_email_obj.correct_format] + '@' + i_email_obj.website_address
        # ------------------------ get to email end ------------------------
        # ------------------------ testing self start ------------------------
        # if output_to_email != os.environ.get('RUN_TEST_EMAIL'):
        #   continue
        # ------------------------ testing self end ------------------------
        # ------------------------ check if email already sent start ------------------------
        db_sent_email_obj = EmailSentObj.query.filter_by(subject=output_subject,to_email=output_to_email).first()
        if db_sent_email_obj != None and db_sent_email_obj != []:
          continue
        # ------------------------ check if email already sent end ------------------------
        # ------------------------ send email start ------------------------
        send_email_template_function(output_to_email, output_subject, output_body)
        # ------------------------ send email end ------------------------
        # ------------------------ add to email sent table start ------------------------
        try:
          new_row = EmailSentObj(
            id=create_uuid_function('sent_'),
            created_timestamp=create_timestamp_function(),
            from_user_id_fk='marketing',
            to_email=output_to_email,
            subject=output_subject,
            body=output_body
          )
          db.session.add(new_row)
          db.session.commit()
        except:
          pass
        # ------------------------ add to email sent table end ------------------------
      # ------------------------ loop emails end ------------------------
      return redirect(url_for('cv_views_admin.admin_email_function', url_redirect_code='s12'))
  return render_template('interior/admin_templates/email_template/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
