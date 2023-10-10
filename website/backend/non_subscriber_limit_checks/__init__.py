# ------------------------ imports start ------------------------
from website import db
from website.models import CvObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def non_subscriber_limit_add_cv_function(current_user):
  count_limit = 5
  limit_reached = False
  try:
    db_obj = CvObj.query.filter_by(fk_user_id=current_user.id).all()
    current_count = len(db_obj)
    if current_count >= count_limit:
      limit_reached = True
  except:
    pass
  return limit_reached
# ------------------------ individual function end ------------------------
