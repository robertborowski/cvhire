# ------------------------ imports start ------------------------
from website.models import CvObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def additional_cv_info_from_db_function(current_user_id, input_dict):
  # ------------------------ get from db start ------------------------
  db_cv_obj = CvObj.query.filter_by(fk_user_id=current_user_id,id=input_dict['fk_cv_id']).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ if none start ------------------------
  if db_cv_obj == None:
    input_dict['candidate_name'] = ''
    input_dict['candidate_email'] = ''
    input_dict['candidate_phone'] = ''
    return input_dict
  # ------------------------ if none end ------------------------
  # ------------------------ pull data start ------------------------
  if db_cv_obj.candidate_name == None:
    input_dict['candidate_name'] = ''
  else:
    input_dict['candidate_name'] = db_cv_obj.candidate_name
  if db_cv_obj.candidate_email == None:
    input_dict['candidate_email'] = ''
  else:
    input_dict['candidate_email'] = db_cv_obj.candidate_email
  if db_cv_obj.candidate_phone == None:
    input_dict['candidate_phone'] = ''
  else:
    input_dict['candidate_phone'] = db_cv_obj.candidate_phone
  # ------------------------ pull data end ------------------------
  return input_dict
# ------------------------ individual function end ------------------------
