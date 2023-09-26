# ------------------------ imports start ------------------------
from website import db
from website.models import RolesObj
from website.backend.convert import objs_to_arr_of_dicts_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_roles_function(current_user, page_dict, input_status):
  # ------------------------ set variables start ------------------------
  page_dict['role_status_type'] = input_status
  page_dict['total_roles'] = 0
  db_roles_obj = None
  # ------------------------ set variables end ------------------------
  # ------------------------ pull from db start ------------------------
  if input_status == 'all':
    db_roles_obj = RolesObj.query.filter_by(fk_user_id=current_user.id).order_by(RolesObj.name).all()
  else:
    db_roles_obj = RolesObj.query.filter_by(fk_user_id=current_user.id,status=input_status).order_by(RolesObj.name).all()
  # ------------------------ pull from db end ------------------------
  # ------------------------ assign variables start ------------------------
  page_dict['total_roles'] = len(db_roles_obj)
  page_dict['total_roles_arr_of_dicts'] = objs_to_arr_of_dicts_function(db_roles_obj, 'roles')
  # ------------------------ assign variables end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------
