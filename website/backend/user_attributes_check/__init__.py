# ------------------------ imports start ------------------------
from website.models import UserAttributesObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def onboarding_checks_function(current_user):
  # ------------------------ check all attributes table start ------------------------
  attribute_arr = ['attribute_marketing']
  for i_attribute in attribute_arr:
    attribute_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_key=i_attribute).first()
    if attribute_obj == None or attribute_obj == []:
      return i_attribute
  # ------------------------ check all attributes table end ------------------------
  # ------------------------ check if email verified start ------------------------
  if current_user.verified_email == False:
    return 'verify'
  # ------------------------ check if email verified end ------------------------
  return None
# ------------------------ individual function end ------------------------