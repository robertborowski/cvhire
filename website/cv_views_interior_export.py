# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import EmailSentObj, GradedObj
import os
from datetime import datetime
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function, postgres_connect_open_function, postgres_connect_close_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import dashboard_section_links_dict_export_function, export_status_codes_function
from website.backend.sql_queries import select_query_v6_function
import csv
import io
from website.backend.sendgrid import send_email_with_attachment_template_function, send_email_template_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_export = Blueprint('cv_views_interior_export', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_export.route('/export', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/', methods=['GET', 'POST'])
@login_required
def cv_export_function():
  return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_export.route('/export/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_export.route('/export/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def export_dashboard_function(url_status_code='export_results', url_redirect_code=None):
  # ------------------------ if user anonymous start ------------------------
  if 'anonymous_user' in current_user.id:
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e25'))
  # ------------------------ if user anonymous end ------------------------
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user, url_redirect_code, url_replace_value=url_status_code)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if not verified start ------------------------
  if page_dict['verified_email'] == False:
    return redirect(url_for('cv_views_interior_account.force_verify_page_function'))
  # ------------------------ if not verified end ------------------------
  # ------------------------ check if status code is valid start ------------------------
  status_codes_arr = export_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'export'
  page_dict['nav_header'] = True
  page_dict['view_reason'] = 'export'
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_export_function()
  # ------------------------ get list end ------------------------
  # ------------------------ get total results start ------------------------
  db_grade_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').all()
  page_dict['content_total_rows'] = 0
  try:
    page_dict['content_total_rows'] = len(db_grade_obj)
  except:
    pass
  # ------------------------ get total results end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Export'
  page_dict['dashboard_action'] = 'Export results'
  page_dict['dashboard_action_link'] = '/export/export_results'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'export_results':
    correct_template = 'interior/export_pages/results/index.html'
  # ------------------------ choose correct template end ------------------------
  # ------------------------ add email start ------------------------
  page_dict['current_user_email'] = current_user.email
  # ------------------------ add email end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ non subscriber limit check start ------------------------
    if page_dict['subscribe_status'] != 'active':
      return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results', url_redirect_code='e16'))
    # ------------------------ non subscriber limit check end ------------------------
    try:
      # ------------------------ open connection start ------------------------
      postgres_connection, postgres_cursor = postgres_connect_open_function()
      # ------------------------ open connection end ------------------------
      # ------------------------ get sql results start ------------------------
      results_arr_of_dicts = select_query_v6_function(postgres_cursor, current_user.id)
      if results_arr_of_dicts != [] and results_arr_of_dicts != None:
        column_names = [desc[0] for desc in postgres_cursor.description]
        # ------------------------ get sql results end ------------------------
        # ------------------------ close connection start ------------------------
        postgres_connect_close_function(postgres_connection, postgres_cursor)
        # ------------------------ close connection end ------------------------
        # ------------------------ csv in memory start ------------------------
        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerow(column_names)
        csv_writer.writerows(results_arr_of_dicts)
        csv_content = output.getvalue()
        output.close()
        # ------------------------ csv in memory end ------------------------
        # ------------------------ set variables start ------------------------
        csv_file_name = create_uuid_function('export_')
        today = datetime.today()
        formatted_date = today.strftime('%Y-%m-%d')
        output_subject = ''
        # ------------------------ set variables end ------------------------
        # ------------------------ send email with attachment start ------------------------
        try:
          output_subject = f'Export results {formatted_date} | CVhire'
          output_body = f'Your CVhire export is attached.'
          send_email_with_attachment_template_function(current_user.email, output_subject, output_body, csv_content, csv_file_name)
        except Exception as e:
          print(f'Error sending attachment: {e}')
          return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results', url_redirect_code='s10'))
        # ------------------------ send email with attachment end ------------------------
        # ------------------------ add to email sent table start ------------------------
        try:
          new_row = EmailSentObj(
            id=create_uuid_function('sent_'),
            created_timestamp=create_timestamp_function(),
            from_user_id_fk='standard',
            to_email=current_user.email,
            subject=output_subject,
            body='export results csv sent'
          )
          db.session.add(new_row)
          db.session.commit()
        except:
          pass
        # ------------------------ add to email sent table end ------------------------
        # ------------------------ email self notifications start ------------------------
        try:
          output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
          output_subject_self = f'New export'
          output_body = f'{current_user.email} | {output_subject}'
          send_email_template_function(output_to_email, output_subject_self, output_body)
        except:
          pass
        # ------------------------ email self notifications end ------------------------
    except Exception as e:
      print(f'Error export_dashboard_function: {e}')
      return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results', url_redirect_code='s10'))
    return redirect(url_for('cv_views_interior_export.export_dashboard_function', url_status_code='export_results', url_redirect_code='s8'))
  # ------------------------ post end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
