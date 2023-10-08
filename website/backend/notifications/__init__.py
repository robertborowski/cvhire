# ------------------------ imports start ------------------------
from website.models import NotificationsObj
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def check_create_default_notifications_function(current_user):
  db_obj = NotificationsObj.query.filter_by(fk_user_id=current_user.id,topic='welcome').first()
  if db_obj == None or db_obj == []:
    # ------------------------ new row start ------------------------
    try:
      new_row = NotificationsObj(
        id=create_uuid_function('notification_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        status='unread',
        topic='welcome',
        message='Welcome to CVhire, the #1 AI tool for resume screening.'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ new row end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def notifications_unread_function(current_user):
  # ------------------------ check if defaults exist start ------------------------
  check_create_default_notifications_function(current_user)
  # ------------------------ check if defaults exist end ------------------------
  # ------------------------ get unread start ------------------------
  try:
    notifications_unread = False
    db_obj = NotificationsObj.query.filter_by(fk_user_id=current_user.id,status='unread').all()
    if db_obj != None and db_obj != []:
      notifications_unread = True
  except Exception as e:
    print(f'Error notifications_unread_function: {e}')
    pass
  # ------------------------ get unread end ------------------------
  return notifications_unread
# ------------------------ individual function end ------------------------
