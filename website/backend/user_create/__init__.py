# ------------------------ imports start ------------------------
import os
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.models import UserObj, UserAttributesObj
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website.backend.user_inputs import get_company_name_function
from website.backend.sendgrid import send_email_template_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def create_user_function(ui_email, ui_password, ui_full_name):
  new_user_id = create_uuid_function('user_')
  # ------------------------ create new user in db start ------------------------
  new_row = UserObj(
    id=new_user_id,
    created_timestamp=create_timestamp_function(),
    email=ui_email.lower(),
    password=generate_password_hash(ui_password, method="sha256")
  )
  db.session.add(new_row)
  db.session.commit()
  # ------------------------ create new user in db end ------------------------
  # ------------------------ keep user logged in start ------------------------
  login_user(new_row, remember=True)
  # ------------------------ keep user logged in end ------------------------
  # ------------------------ new attribute start ------------------------
  new_row = UserAttributesObj(
    id=create_uuid_function('attribute_'),
    created_timestamp=create_timestamp_function(),
    fk_user_id=new_user_id,
    attribute_key='full_name',
    attribute_value=ui_full_name
  )
  db.session.add(new_row)
  db.session.commit()
  # ------------------------ new attribute end ------------------------
  # ------------------------ new attribute 2 start ------------------------
  new_row = UserAttributesObj(
    id=create_uuid_function('attribute_'),
    created_timestamp=create_timestamp_function(),
    fk_user_id=new_user_id,
    attribute_key='company_name',
    attribute_value=get_company_name_function(ui_email.lower())
  )
  db.session.add(new_row)
  db.session.commit()
  # ------------------------ new attribute 2 end ------------------------
  # ------------------------ new attribute 3 start ------------------------
  new_row = UserAttributesObj(
    id=create_uuid_function('attribute_'),
    created_timestamp=create_timestamp_function(),
    fk_user_id=new_user_id,
    attribute_key='profile_img',
    attribute_value='https://cvhirepublicobjects.s3.us-east-2.amazonaws.com/logo_v2_green.png'
  )
  db.session.add(new_row)
  db.session.commit()
  # ------------------------ new attribute 3 end ------------------------
  # ------------------------ new attribute 4 start ------------------------
  new_row = UserAttributesObj(
    id=create_uuid_function('attribute_'),
    created_timestamp=create_timestamp_function(),
    fk_user_id=new_user_id,
    attribute_key='verified_email',
    attribute_value='not_verified'
  )
  db.session.add(new_row)
  db.session.commit()
  # ------------------------ new attribute 4 end ------------------------
  # ------------------------ email self start ------------------------
  if ui_email != os.environ.get('RUN_TEST_EMAIL'):
    try:
      output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
      output_subject = f'New signup: {ui_email}'
      output_body = f'New signup: {ui_email}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
  # ------------------------ email self end ------------------------
  return True
# ------------------------ individual function end ------------------------
