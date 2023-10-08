# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from website.models import UserObj, EmailSentObj, UserAttributesObj
from website.backend.static_lists import navbar_link_dict_function, navbar_link_dict_function_v2
from website.backend.alerts import get_alert_message_function
from website.backend.notifications import notifications_unread_function
# ------------------------ imports end ------------------------

# ------------------------ individual route start ------------------------
def pre_page_load_checks_function(current_user, url_redirect_code=None, url_replace_value=None):
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  # ------------------------ get error message start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = get_alert_message_function(url_redirect_code)
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ get error message end ------------------------
  # ------------------------ locked status start ------------------------
  page_dict['current_user_locked'] = False
  if current_user.locked == True:
    page_dict['current_user_locked'] = True
  # ------------------------ locked status end ------------------------
  # ------------------------ get company name start ------------------------
  db_attribute_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='company_name').first()
  page_dict['company_name'] = db_attribute_obj.attribute_value
  # ------------------------ get company name start ------------------------
  # ------------------------ get profile img start ------------------------
  db_attribute_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='profile_img').first()
  page_dict['profile_img'] = db_attribute_obj.attribute_value
  # ------------------------ get profile img end ------------------------
  # ------------------------ get current site start ------------------------
  page_dict['navbar_link_current'] = str(request.url_rule.rule)
  # ------------------------ special case roles start ------------------------
  try:
    if '<url_status_code>' in page_dict['navbar_link_current']:
      page_dict['navbar_link_current'] = str(request.url_rule.rule).replace('<url_status_code>', url_replace_value)
  except:
    pass
  # ------------------------ special case roles end ------------------------
  if page_dict['navbar_link_current'][-1] == '/':
    page_dict['navbar_link_current'] = page_dict['navbar_link_current'][:-1]
  # ------------------------ get current site end ------------------------
  # ------------------------ get navbar sites start ------------------------
  navbar_link_dict = navbar_link_dict_function()
  page_dict['navbar_link_dict'] = navbar_link_dict
  navbar_link_dict_v2 = navbar_link_dict_function_v2()
  page_dict['navbar_link_dict_v2'] = navbar_link_dict_v2
  # ------------------------ get navbar sites end ------------------------
  # ------------------------ new unread notifications check start ------------------------
  page_dict['notifications_unread'] = notifications_unread_function(current_user)
  # ------------------------ new unread notifications check end ------------------------
  """
  # ------------------------ onboarding checks start ------------------------
  onbaording_status = onboarding_checks_function(current_user)
  if onbaording_status == 'verify':
    page_dict['verified_email_status'] = False
  if onbaording_status != None:
    return redirect(url_for('cv_views_interior.cv_feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  """
  return page_dict
# ------------------------ individual route end ------------------------
