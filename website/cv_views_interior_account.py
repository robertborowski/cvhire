# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website import db
from website.models import UserAttributesObj, EmailSentObj, StripePaymentOptionsObj, StripeCheckoutSessionObj, ConversionTrackingObj
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.connection import redis_connect_open_function
from website.backend.pre_page_load_checks import pre_page_load_checks_function
from website.backend.static_lists import dashboard_section_links_dict_account_function, roles_table_links_function, account_status_codes_function, get_default_profile_imgs_function
from website.backend.sanitize import sanitize_chars_function_v1, sanitize_chars_function_v2, sanitize_image_option_function
from website.backend.db_obj_checks import get_user_content_function
from website.backend.convert import convert_obj_row_to_dict_function
from website.backend.sanitize import sanitize_fullname_function
from website.backend.sendgrid import send_email_template_function
import os
from website.backend.uploads_user import allowed_img_file_upload_function, get_file_suffix_function
from website.backend.aws_logic import upload_public_file_to_aws_s3_function
import stripe
from website.backend.stripe import check_create_stripe_attributes_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_interior_account = Blueprint('cv_views_interior_account', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/', methods=['GET', 'POST'])
@login_required
def cv_account_function():
  return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/settings', methods=['GET', 'POST'])
@cv_views_interior_account.route('/settings/', methods=['GET', 'POST'])
@login_required
def cv_settings_function():
  return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account/<url_status_code>', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/<url_status_code>/', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/<url_status_code>/<url_redirect_code>', methods=['GET', 'POST'])
@cv_views_interior_account.route('/account/<url_status_code>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def cv_account_dashboard_function(url_status_code='user', url_redirect_code=None):
  # ------------------------ if user anonymous start ------------------------
  if 'anonymous_user' in current_user.id:
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='e24'))
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
  status_codes_arr = account_status_codes_function()
  if url_status_code not in status_codes_arr:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e10'))
  # ------------------------ check if status code is valid end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['url_status_code'] = url_status_code
  page_dict['starting_route'] = 'account'
  page_dict['nav_header'] = True
  # ------------------------ get status code end ------------------------
  # ------------------------ get list start ------------------------
  page_dict['dashboard_section_links_dict'] = dashboard_section_links_dict_account_function()
  # ------------------------ get list end ------------------------
  # ------------------------ dashboard variables start ------------------------
  page_dict['dashboard_name'] = 'Account'
  # ------------------------ dashboard variables end ------------------------
  # ------------------------ section start ------------------------
  # ------------------------ get content start ------------------------
  page_dict = get_user_content_function(current_user, page_dict, url_status_code, page_dict['starting_route'])
  # ------------------------ get content end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['current_user_email'] = current_user.email
  if url_status_code == 'user':
    page_dict['view_reason'] = 'edit_account'
  if url_status_code == 'settings':
    page_dict['view_reason'] = 'edit_settings'
  # ------------------------ set variables end ------------------------
  # ------------------------ get stock photos start ------------------------
  page_dict['default_profile_img_dict'] = get_default_profile_imgs_function()
  # ------------------------ get stock photos end ------------------------
  # ------------------------ check/create stripe rows start ------------------------
  check_create_stripe_attributes_function(current_user.id)
  # ------------------------ check/create stripe rows end ------------------------
  # ------------------------ paid subscription time start ------------------------
  if page_dict['subscribe_status'] == 'active':
    db_sub_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='fk_stripe_subscription_id').first()
    page_dict['subscriber_since'] = db_sub_obj.created_timestamp
  # ------------------------ paid subscription time end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ post #1 start ------------------------
    if url_status_code == 'user':
      # ------------------------ get user inputs start ------------------------
      ui_full_name = request.form.get('uiFullName')
      ui_company_name = request.form.get('uiCompanyName')
      ui_profile_img = request.form.get('uiRadioProfileImg')
      ui_file_uploaded = request.files.get('uiFormFileSingleUpload')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ check if img uploaded start ------------------------
      ui_img_uploaded = False
      if ui_file_uploaded.filename != '':
        ui_img_uploaded = True
      # ------------------------ check if img uploaded end ------------------------
      # ------------------------ non subscriber limit check start ------------------------
      if ui_img_uploaded == True and page_dict['subscribe_status'] != 'active':
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e17'))
      # ------------------------ non subscriber limit check end ------------------------
      # ------------------------ sanitize user inputs start ------------------------
      ui_full_name_check = sanitize_fullname_function(ui_full_name)
      ui_company_name_check = sanitize_fullname_function(ui_company_name)
      ui_profile_img_check = False
      if ui_img_uploaded == False:
        ui_profile_img_check = sanitize_image_option_function(ui_profile_img, page_dict['default_profile_img_dict'])
      ui_file_uploaded_check = False
      if ui_img_uploaded == True:
        ui_file_uploaded_check = allowed_img_file_upload_function(ui_file_uploaded.filename)
      # ------------------------ sanitize user inputs end ------------------------
      # ------------------------ redirect error start ------------------------
      if ui_full_name_check == False or ui_company_name_check == False:
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e8'))
      if ui_img_uploaded == False and ui_profile_img_check == False:
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e10'))
      if ui_img_uploaded == True and ui_file_uploaded_check == False:
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='e10'))
      # ------------------------ redirect error end ------------------------
      # ------------------------ upload aws img start ------------------------
      if ui_img_uploaded == True and ui_file_uploaded_check == True:
        file_name_suffix = get_file_suffix_function(ui_file_uploaded.filename)
        new_name = create_uuid_function('customLogo_') + file_name_suffix
        upload_public_file_to_aws_s3_function(ui_file_uploaded, new_name)
        ui_profile_img = 'https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/' + new_name
        # ------------------------ email self start ------------------------
        try:
          output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
          output_subject = f'{current_user.email} | uploaded company logo to AWS'
          output_body = f'{current_user.email} | uploaded company logo to AWS'
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
        # ------------------------ email self end ------------------------
      # ------------------------ upload aws img end ------------------------
      # ------------------------ update db start ------------------------
      change_occurred = False
      # ------------------------ full name start ------------------------
      db_full_name_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='full_name').first()
      if db_full_name_obj.attribute_value != ui_full_name:
        db_full_name_obj.attribute_value = ui_full_name
        change_occurred = True
      # ------------------------ full name end ------------------------
      # ------------------------ company name start ------------------------
      db_company_name_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='company_name').first()
      if db_company_name_obj.attribute_value != ui_company_name:
        db_company_name_obj.attribute_value = ui_company_name
        change_occurred = True
      # ------------------------ company name end ------------------------
      # ------------------------ profile pic start ------------------------
      db_profile_img_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='profile_img').first()
      if db_profile_img_obj.attribute_value != ui_profile_img:
        db_profile_img_obj.attribute_value = ui_profile_img
        change_occurred = True
      # ------------------------ profile pic end ------------------------
      if change_occurred == True:
        db.session.commit()
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='s5'))
      if change_occurred == False:
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user', url_redirect_code='i1'))
      # ------------------------ update db end ------------------------
    # ------------------------ post #1 end ------------------------
    # ------------------------ post #2 start ------------------------
    elif url_status_code == 'settings':
      # ------------------------ delete all previous checkout drafts start ------------------------
      StripeCheckoutSessionObj.query.filter_by(fk_user_id=current_user.id,status='draft').delete()
      # ------------------------ delete all previous checkout drafts end ------------------------
      # ------------------------ get user inputs start ------------------------
      ui_subscription_choice = request.form.get('radioSubscriptionOption')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize user inputs start ------------------------
      if ui_subscription_choice != 'yearly' and ui_subscription_choice != 'monthly':
        return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings', url_redirect_code='e10'))
      # ------------------------ sanitize user inputs end ------------------------
      # ------------------------ get from db start ------------------------
      db_stripe_obj = StripePaymentOptionsObj.query.filter_by(name=ui_subscription_choice).order_by(StripePaymentOptionsObj.created_timestamp.desc()).first()
      # ------------------------ get from db end ------------------------
      # ------------------------ select variable start ------------------------
      price_id = None
      stripe_env = 'production'
      if stripe_env == 'testing':
        price_id = db_stripe_obj.fk_stripe_price_id_testing
      else:
        price_id = db_stripe_obj.fk_stripe_price_id
      # ------------------------ select variable end ------------------------
      # ------------------------ stripe checkout start ------------------------
      try:
        checkout_session = stripe.checkout.Session.create(
          line_items=[
            {
            'price': price_id,
            'quantity': 1,
            },
          ],
          mode='subscription',
          success_url='https://cvhire.com/subscription/success',
          cancel_url='https://cvhire.com/account/settings',
          metadata={
            'fk_user_id': current_user.id
          }
        )
        # ------------------------ create db row start ------------------------
        # This is so I can easily get the customer id and subscription id in a future lookup
        new_checkout_session_obj = StripeCheckoutSessionObj(
          id = create_uuid_function('checkout_'),
          created_timestamp = create_timestamp_function(),
          fk_user_id = current_user.id,
          status = 'draft',
          fk_checkout_session_id = checkout_session.id
        )
        db.session.add(new_checkout_session_obj)
        db.session.commit()
        # ------------------------ create db row end ------------------------
      except Exception as e:
        return str(e)
      # ------------------------ this line of code is needed to actually redirec to stripe checkout page start ------------------------
      return redirect(checkout_session.url, code=303)
      # ------------------------ this line of code is needed to actually redirec to stripe checkout page end ------------------------
      # ------------------------ stripe checkout end ------------------------
    # ------------------------ post #2 end ------------------------
  # ------------------------ post end ------------------------
  # ------------------------ choose correct template start ------------------------
  correct_template = ''
  if url_status_code == 'user':
    correct_template = 'interior/account/user/index.html'
  if url_status_code == 'settings':
    correct_template = 'interior/account/settings_acc/index.html'
  # ------------------------ choose correct template end ------------------------
  return render_template(correct_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/verify/resend')
@cv_views_interior_account.route('/verify/resend/')
@login_required
def force_verify_page_function():
  # ------------------------ pre load page checks start ------------------------
  page_dict = pre_page_load_checks_function(current_user)
  if page_dict['current_user_locked'] == True:
    return redirect(url_for('cv_views_interior.cv_locked_function'))
  # ------------------------ pre load page checks end ------------------------
  # ------------------------ if already verified start ------------------------
  if page_dict['verified_email'] == True:
    return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='s10'))
  # ------------------------ if already verified end ------------------------
  # ------------------------ auto send first email start ------------------------
  db_sent_obj = EmailSentObj.query.filter_by(from_user_id_fk=current_user.id,subject='Verify email | CVhire').order_by(EmailSentObj.created_timestamp.desc()).first()
  if db_sent_obj == None or db_sent_obj == []:
    return redirect(url_for('cv_views_interior_account.account_verify_send_function'))
  # ------------------------ auto send first email end ------------------------
  # ------------------------ get status code start ------------------------
  page_dict['nav_header'] = False
  page_dict['view_reason'] = 'verify_pending'
  page_dict['current_user_email'] = current_user.email
  # ------------------------ get status code end ------------------------
  return render_template('interior/account/settings_acc/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account/verify/email/send')
@cv_views_interior_account.route('/account/verify/email/send/')
@login_required
def account_verify_send_function():
  # ------------------------ set variables start ------------------------
  verification_code = ''
  # ------------------------ set variables end ------------------------
  # ------------------------ check if verify code exists start ------------------------
  db_verify_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='verification_email_code').first()
  # ------------------------ check if verify code exists end ------------------------
  # ------------------------ if verify code does not exist start ------------------------
  if db_verify_obj == None or db_verify_obj == []:
    verification_code = create_uuid_function('verify_')
    # ------------------------ new row start ------------------------
    new_row = UserAttributesObj(
      id=create_uuid_function('attribute_'),
      created_timestamp=create_timestamp_function(),
      fk_user_id=current_user.id,
      attribute_key='verification_email_code',
      attribute_value=verification_code
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ new row end ------------------------
  # ------------------------ if verify code does not exist end ------------------------
  # ------------------------ if verify code does exist start ------------------------
  else:
    verification_code = db_verify_obj.attribute_value
  # ------------------------ if verify code does exist end ------------------------
  # ------------------------ set variables start ------------------------
  final_link = ''
  if os.environ.get('TESTING') == 'true':
    final_link = f'http://127.0.0.1/account/verify/email/receive/{verification_code}'
  else:
    final_link = f'https://cvhire.com/account/verify/email/receive/{verification_code}'
  output_subject = f'Verify email | CVhire'
  output_body = f'Click to verify email {final_link}'
  # ------------------------ set variables end ------------------------
  # ------------------------ send email to user start ------------------------
  try:
    send_email_template_function(current_user.email, output_subject, output_body)
  except:
    pass
  # ------------------------ send email to user end ------------------------
  # ------------------------ add to email sent table start ------------------------
  try:
    new_row = EmailSentObj(
      id=create_uuid_function('sent_'),
      created_timestamp=create_timestamp_function(),
      from_user_id_fk=current_user.id,
      to_email=current_user.email,
      subject=output_subject,
      body=output_body
    )
    db.session.add(new_row)
    db.session.commit()
  except:
    pass
  # ------------------------ add to email sent table end ------------------------
  # ------------------------ lock account if too many emails start ------------------------
  db_emails_obj = EmailSentObj.query.filter_by(from_user_id_fk=current_user.id,subject=output_subject).all()
  try:
    if len(db_emails_obj) >= 7:
      current_user.locked = True
      db.session.commit()
  except:
    pass
  # ------------------------ lock account if too many emails end ------------------------
  return redirect(url_for('cv_views_interior_account.force_verify_page_function', url_redirect_code='s3'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/account/verify/email/receive/<url_verify_code>')
@cv_views_interior_account.route('/account/verify/email/receive/<url_verify_code>/')
# @login_required
def account_verify_receive_function(url_verify_code=None):
  # ------------------------ reroute start ------------------------
  if url_verify_code == None:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user'))
  # ------------------------ reroute end ------------------------
  # ------------------------ pull from db start ------------------------
  db_code_obj = UserAttributesObj.query.filter_by(attribute_value=url_verify_code).first()
  # ------------------------ pull from db end ------------------------
  # ------------------------ if not found start ------------------------
  if db_code_obj == None or db_code_obj == []:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user'))
  # ------------------------ if not found end ------------------------
  # ------------------------ update attribute start ------------------------
  user_to_verify = db_code_obj.fk_user_id
  db_user_obj = UserAttributesObj.query.filter_by(fk_user_id=user_to_verify,attribute_key='verified_email').first()
  # ------------------------ update attribute end ------------------------
  # ------------------------ if not found start ------------------------
  if db_user_obj == None or db_user_obj == []:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='user'))
  # ------------------------ if not found end ------------------------
  # ------------------------ update db start ------------------------
  db_user_obj.attribute_value = 'yes_verified'
  db.session.commit()
  # ------------------------ update db end ------------------------
  # ------------------------ delete verify code row start ------------------------
  UserAttributesObj.query.filter_by(attribute_value=url_verify_code).delete()
  db.session.commit()
  # ------------------------ delete verify code row end ------------------------
  # ------------------------ conversion tracking start ------------------------
  db_conversion_obj = ConversionTrackingObj.query.filter_by(fk_user_id=user_to_verify,event='conversion_signup').first()
  if db_conversion_obj == None or db_conversion_obj == []:
    # ------------------------ new row start ------------------------
    try:
      new_row = ConversionTrackingObj(
        id=create_uuid_function('conversion_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=user_to_verify,
        event='conversion_signup',
        status='done'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ new row end ------------------------
    # ------------------------ set variables start ------------------------
    page_dict = {}
    page_dict['nav_header'] = False
    page_dict['alert_message_dict'] = {}
    page_dict['alert_message_dict']['message'] = ''
    page_dict['conversion_type'] = 'signup'
    # ------------------------ set variables end ------------------------
    # ------------------------ email self notifications start ------------------------
    try:
      output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
      output_subject = f'New user: Email verified successfully'
      output_body = f'email: {current_user.email}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self notifications end ------------------------
    return render_template('interior/conversion_tracking/index.html', page_dict_html=page_dict)
  # ------------------------ conversion tracking end ------------------------
  return redirect(url_for('cv_views_interior_ai.cv_dashboard_function', url_status_code='one-role-many-cvs', url_redirect_code='s10'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_interior_account.route('/subscription/success')
@cv_views_interior_account.route('/subscription/success/')
@login_required
def subscription_success_function():
  # ------------------------ get from db start ------------------------
  db_checkout_session_obj = StripeCheckoutSessionObj.query.filter_by(fk_user_id=current_user.id,status='draft').order_by(StripeCheckoutSessionObj.created_timestamp.desc()).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ if not found start ------------------------
  if db_checkout_session_obj == None or db_checkout_session_obj == '' or db_checkout_session_obj == False:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings', url_redirect_code='e10'))
  # ------------------------ if not found end ------------------------
  # ------------------------ stripe lookup start ------------------------
  stripe_checkout_session_obj = stripe.checkout.Session.retrieve(db_checkout_session_obj.fk_checkout_session_id)
  # ------------------------ if not found start ------------------------
  if stripe_checkout_session_obj == None:
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings', url_redirect_code='e10'))
  # ------------------------ if not found end ------------------------
  # ------------------------ if not finalized start ------------------------
  stripe_checkout_session_payment_status = stripe_checkout_session_obj.payment_status
  if stripe_checkout_session_payment_status != 'paid':
    return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings', url_redirect_code='e10'))
  # ------------------------ if not finalized end ------------------------
  stripe_customer_id = stripe_checkout_session_obj.customer
  stripe_subscription_id = stripe_checkout_session_obj.subscription
  # ------------------------ stripe lookup end ------------------------
  # ------------------------ update db start ------------------------
  db_customer_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='fk_stripe_customer_id').first()
  db_customer_obj.attribute_value = stripe_customer_id
  db_subscription_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='fk_stripe_subscription_id').first()
  db_subscription_obj.attribute_value = stripe_subscription_id
  db_subscription_obj.created_timestamp = create_timestamp_function()
  db_checkout_session_obj.status = 'final'
  db.session.commit()
  # ------------------------ update db end ------------------------
  # ------------------------ send email to user start ------------------------
  try:
    output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
    output_subject = f'NEW SUBSCRIPTION: {current_user.email} | CVhire'
    output_body = f'NEW SUBSCRIPTION: {current_user.email} | CVhire'
    send_email_template_function(output_to_email, output_subject, output_body)
  except:
    pass
  # ------------------------ send email to user end ------------------------
  # ------------------------ conversion tracking start ------------------------
  db_conversion_obj = ConversionTrackingObj.query.filter_by(fk_user_id=current_user.id,event='conversion_subscribed').first()
  if db_conversion_obj == None or db_conversion_obj == []:
    # ------------------------ new row start ------------------------
    try:
      new_row = ConversionTrackingObj(
        id=create_uuid_function('conversion_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        event='conversion_subscribed',
        status='done'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ new row end ------------------------
    # ------------------------ set variables start ------------------------
    page_dict = {}
    page_dict['nav_header'] = False
    page_dict['alert_message_dict'] = {}
    page_dict['alert_message_dict']['message'] = ''
    page_dict['conversion_type'] = 'subscription'
    # ------------------------ set variables end ------------------------
    return render_template('interior/conversion_tracking/index.html', page_dict_html=page_dict)
  # ------------------------ conversion tracking end ------------------------
  return redirect(url_for('cv_views_interior_account.cv_account_dashboard_function', url_status_code='settings', url_redirect_code='s11'))
# ------------------------ individual route end ------------------------
