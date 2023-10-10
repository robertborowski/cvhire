# ------------------------ imports start ------------------------
from website import db
from website.models import UserAttributesObj
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
import stripe
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def check_create_stripe_attributes_function(current_user_id):
  # ------------------------ create attribute id start ------------------------
  db_customer_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user_id,attribute_key='fk_stripe_customer_id').first()
  if db_customer_obj == None or db_customer_obj == []:
    # ------------------------ new attribute start ------------------------
    new_row = UserAttributesObj(
      id=create_uuid_function('attribute_'),
      created_timestamp=create_timestamp_function(),
      fk_user_id=current_user_id,
      attribute_key='fk_stripe_customer_id',
      attribute_value=None
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ new attribute end ------------------------
  # ------------------------ create attribute id end ------------------------
  # ------------------------ create attribute id start ------------------------
  db_subscription_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user_id,attribute_key='fk_stripe_subscription_id').first()
  if db_subscription_obj == None or db_subscription_obj == []:
    # ------------------------ new attribute start ------------------------
    new_row = UserAttributesObj(
      id=create_uuid_function('attribute_'),
      created_timestamp=create_timestamp_function(),
      fk_user_id=current_user_id,
      attribute_key='fk_stripe_subscription_id',
      attribute_value=None
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ new attribute end ------------------------
  # ------------------------ create attribute id end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_stripe_subscription_status_function(current_user_id):
  stripe_subscription_obj = ''
  stripe_status = 'not active'
  try:
    # ------------------------ from db start ------------------------
    db_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user_id,attribute_key='fk_stripe_subscription_id').first()
    # ------------------------ from db end ------------------------
    # ------------------------ stripe subscription status check start ------------------------
    try:
      stripe_subscription_obj = stripe.Subscription.retrieve(db_obj.attribute_value)
      stripe_status = stripe_subscription_obj.status
    except:
      pass
    # ------------------------ stripe subscription status check end ------------------------
  except:
    pass
  return stripe_status
# ------------------------ individual function end ------------------------