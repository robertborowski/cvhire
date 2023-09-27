# ------------------------ imports start ------------------------
from website import db
from website.models import RolesObj, CvObj
from website.backend.convert import objs_to_arr_of_dicts_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_content_function(current_user, page_dict, url_status_code, dashboard_type):
  # ------------------------ set variables start ------------------------
  page_dict['content_total_rows'] = 0
  page_dict['content_total_rows_arr_of_dicts'] = None
  db_roles_obj = None
  # ------------------------ set variables end ------------------------
  # ------------------------ pull from db start ------------------------
  if dashboard_type == 'roles':
    if url_status_code == 'all':
      db_roles_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).filter(RolesObj.status != 'delete').order_by(RolesObj.name).all()
    else:
      db_roles_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(RolesObj.name).all()
  if dashboard_type == 'cv':
    if url_status_code == 'all':
      db_roles_obj = CvObj.query.filter_by(fk_user_id=current_user.id).filter(CvObj.status != 'delete').order_by(CvObj.created_timestamp.desc()).all()
    else:
      db_roles_obj = CvObj.query.filter_by(fk_user_id=current_user.id,status=url_status_code).order_by(CvObj.created_timestamp.desc()).all()
  # ------------------------ pull from db end ------------------------
  # ------------------------ assign variables start ------------------------
  page_dict['content_total_rows'] = len(db_roles_obj)
  if dashboard_type == 'roles':
    page_dict['content_total_rows_arr_of_dicts'] = objs_to_arr_of_dicts_function(db_roles_obj, 'roles')
  if dashboard_type == 'cv':
    page_dict['content_total_rows_arr_of_dicts'] = objs_to_arr_of_dicts_function(db_roles_obj, 'cv')
  # ------------------------ assign variables end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------
