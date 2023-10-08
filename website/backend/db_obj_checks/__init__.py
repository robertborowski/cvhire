# ------------------------ imports start ------------------------
from website import db
from website.models import RolesObj, CvObj, GradedObj, NotificationsObj, UserAttributesObj
from website.backend.convert import objs_to_arr_of_dicts_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_content_function(current_user, page_dict, url_status_code, dashboard_type, sort_option_passed=None):
  # ------------------------ set variables start ------------------------
  page_dict['content_total_rows'] = 0
  page_dict['content_total_rows_arr_of_dicts'] = None
  db_obj = None
  # ------------------------ set variables end ------------------------
  # ------------------------ pull from db start ------------------------
  # ------------------------ roles start ------------------------
  if dashboard_type == 'roles':
    if url_status_code == 'all':
      # ------------------------ sorting custom start ------------------------
      if sort_option_passed == 'sort_name_a':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).filter(RolesObj.status != 'delete').order_by(RolesObj.name).all()
      elif sort_option_passed == 'sort_name_z':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).filter(RolesObj.status != 'delete').order_by(RolesObj.name.desc()).all()
      elif sort_option_passed == 'sort_time_a':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).filter(RolesObj.status != 'delete').order_by(RolesObj.created_timestamp).all()
      elif sort_option_passed == 'sort_time_z':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).filter(RolesObj.status != 'delete').order_by(RolesObj.created_timestamp.desc()).all()
      # ------------------------ sorting custom end ------------------------
      # ------------------------ sorting default start ------------------------
      else:
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).filter(RolesObj.status != 'delete').order_by(RolesObj.name).all()
      # ------------------------ sorting default end ------------------------
    else:
      # ------------------------ sorting custom start ------------------------
      if sort_option_passed == 'sort_name_a':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(RolesObj.name).all()
      elif sort_option_passed == 'sort_name_z':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(RolesObj.name.desc()).all()
      elif sort_option_passed == 'sort_time_a':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(RolesObj.created_timestamp).all()
      elif sort_option_passed == 'sort_time_z':
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(RolesObj.created_timestamp.desc()).all()
      # ------------------------ sorting custom end ------------------------
      # ------------------------ sorting default start ------------------------
      else:
        db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(RolesObj.name).all()
      # ------------------------ sorting default end ------------------------
  # ------------------------ roles end ------------------------
  # ------------------------ cv start ------------------------
  if dashboard_type == 'cv':
    if url_status_code == 'all':
      # ------------------------ sorting custom start ------------------------
      if sort_option_passed == 'sort_name_a':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id).filter(CvObj.status != 'delete').order_by(CvObj.candidate_name).all()
      elif sort_option_passed == 'sort_name_z':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id).filter(CvObj.status != 'delete').order_by(CvObj.candidate_name.desc()).all()
      elif sort_option_passed == 'sort_time_a':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id).filter(CvObj.status != 'delete').order_by(CvObj.created_timestamp).all()
      elif sort_option_passed == 'sort_time_z':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id).filter(CvObj.status != 'delete').order_by(CvObj.created_timestamp.desc()).all()
      # ------------------------ sorting custom end ------------------------
      # ------------------------ sorting default start ------------------------
      else:
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id).filter(CvObj.status != 'delete').order_by(CvObj.candidate_name).all()
      # ------------------------ sorting default end ------------------------
    else:
      # ------------------------ sorting custom start ------------------------
      if sort_option_passed == 'sort_name_a':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(CvObj.candidate_name).all()
      elif sort_option_passed == 'sort_name_z':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(CvObj.candidate_name.desc()).all()
      elif sort_option_passed == 'sort_time_a':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(CvObj.created_timestamp).all()
      elif sort_option_passed == 'sort_time_z':
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(CvObj.created_timestamp.desc()).all()
      # ------------------------ sorting custom end ------------------------
      # ------------------------ sorting default start ------------------------
      else:
        db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(CvObj.candidate_name).all()
      # ------------------------ sorting default end ------------------------
  # ------------------------ cv end ------------------------
  # ------------------------ results start ------------------------
  if dashboard_type == 'results':
    if url_status_code == 'all':
      # ------------------------ sorting custom start ------------------------
      if sort_option_passed == 'sort_name_a':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').order_by(GradedObj.fk_role_name,GradedObj.score.desc(),GradedObj.fk_cv_name).all()
      elif sort_option_passed == 'sort_name_z':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').order_by(GradedObj.fk_role_name.desc(),GradedObj.score.desc(),GradedObj.fk_cv_name).all()
      elif sort_option_passed == 'sort_time_a':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').order_by(GradedObj.created_timestamp).all()
      elif sort_option_passed == 'sort_time_z':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').order_by(GradedObj.created_timestamp.desc()).all()
      # ------------------------ sorting custom end ------------------------
      # ------------------------ sorting default start ------------------------
      else:
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id).filter(GradedObj.status != 'delete').order_by(GradedObj.fk_role_name,GradedObj.score.desc(),GradedObj.fk_cv_name).all()
      # ------------------------ sorting default end ------------------------
    else:
      # ------------------------ sorting custom start ------------------------
      if sort_option_passed == 'sort_name_a':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(GradedObj.fk_role_name,GradedObj.score.desc(),GradedObj.fk_cv_name).all()
      elif sort_option_passed == 'sort_name_z':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(GradedObj.fk_role_name.desc(),GradedObj.score.desc(),GradedObj.fk_cv_name).all()
      elif sort_option_passed == 'sort_time_a':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(GradedObj.created_timestamp).all()
      elif sort_option_passed == 'sort_time_z':
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(GradedObj.created_timestamp.desc()).all()
      # ------------------------ sorting custom end ------------------------
      # ------------------------ sorting default start ------------------------
      else:
        db_obj = GradedObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(GradedObj.fk_role_name,GradedObj.score.desc(),GradedObj.fk_cv_name).all()
      # ------------------------ sorting default end ------------------------
  # ------------------------ results end ------------------------
  # ------------------------ notifications start ------------------------
  if dashboard_type == 'notifications':
    db_obj = NotificationsObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(NotificationsObj.created_timestamp.desc()).all()
  # ------------------------ notifications end ------------------------
  # ------------------------ pull from db end ------------------------
  # ------------------------ assign variables start ------------------------
  page_dict['content_total_rows'] = len(db_obj)
  page_dict['content_total_rows_arr_of_dicts'] = objs_to_arr_of_dicts_function(db_obj, dashboard_type)
  # ------------------------ assign variables end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_content_split_function(current_user, page_dict, item_type):
  # ------------------------ set variables start ------------------------
  page_dict[f'content_total_rows_{item_type}'] = 0
  page_dict[f'content_total_rows_arr_of_dicts_{item_type}'] = None
  db_obj = None
  # ------------------------ set variables end ------------------------
  # ------------------------ pull from db start ------------------------
  # ------------------------ roles start ------------------------
  if item_type == 'roles':
    db_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status='open').order_by(RolesObj.name).all()
  # ------------------------ roles end ------------------------
  # ------------------------ cv start ------------------------
  elif item_type == 'cv':
    db_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status='active').order_by(CvObj.candidate_name).all()
  # ------------------------ cv end ------------------------
  # ------------------------ pull from db end ------------------------
  # ------------------------ assign variables start ------------------------
  page_dict[f'content_total_rows_{item_type}'] = len(db_obj)
  if item_type == 'roles':
    page_dict[f'content_total_rows_arr_of_dicts_{item_type}'] = objs_to_arr_of_dicts_function(db_obj, 'roles')
  if item_type == 'cv':
    page_dict[f'content_total_rows_arr_of_dicts_{item_type}'] = objs_to_arr_of_dicts_function(db_obj, 'cv')
  # ------------------------ assign variables end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_user_content_function(current_user, page_dict, url_status_code, dashboard_type):
  if url_status_code == 'user':
    # ------------------------ set variables start ------------------------
    user_info_dict = {
      'Email': current_user.email,
      'Full name': '',
      'Company': '',
      'Photo': ''
    }
    # ------------------------ set variables end ------------------------
    # ------------------------ pull from db start ------------------------
    db_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='full_name').first()
    user_info_dict['Full name'] = db_obj.attribute_value
    # ------------------------ pull from db end ------------------------
    # ------------------------ pull from db start ------------------------
    db_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='company_name').first()
    user_info_dict['Company'] = db_obj.attribute_value
    # ------------------------ pull from db end ------------------------
    # ------------------------ pull from db start ------------------------
    db_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key='profile_img').first()
    user_info_dict['Photo'] = db_obj.attribute_value
    # ------------------------ pull from db end ------------------------
    page_dict['user_info_dict'] = user_info_dict
  return page_dict
# ------------------------ individual function end ------------------------