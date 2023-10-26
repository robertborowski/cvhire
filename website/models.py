# ------------------------ imports start ------------------------
from email.policy import default
from website import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website import secret_key_ref
# ------------------------ imports end ------------------------

# ------------------------ individual model start ------------------------
# Note: models vs tables: https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
class UserObj(db.Model, UserMixin):   # Only the users object inherits UserMixin, other models do NOT!
  # ------------------------ general start ------------------------
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
  password = db.Column(db.String(150))
  locked = db.Column(db.Boolean, default=False)

  def get_reset_token_function(self, expires_sec=1800):
    serializer_token_obj = Serializer(secret_key_ref, expires_sec)
    return serializer_token_obj.dumps({'dump_load_user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token_function(token_to_search_for):
    serializer_token_obj = Serializer(secret_key_ref)
    try:
      dl_user_id_from_token = serializer_token_obj.loads(token_to_search_for)['dump_load_user_id']
    except:
      return None
    return UserObj.query.get(dl_user_id_from_token)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class UserAttributesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  attribute_key = db.Column(db.String(50))
  attribute_value = db.Column(db.String(1000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailSentObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  from_user_id_fk = db.Column(db.String(150))
  to_email = db.Column(db.String(150))
  subject = db.Column(db.String(1000))
  body = db.Column(db.String(5000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailBlockObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailScrapedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), unique=True)
  unsubscribed = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class RolesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(20))
  name = db.Column(db.String(150))
  about = db.Column(db.String(3000))
  requirements = db.Column(db.String(3000))
  nice_to_haves = db.Column(db.String(3000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CvObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(20))
  cv_upload_name = db.Column(db.String(150))
  cv_aws_id = db.Column(db.String(150))
  candidate_email = db.Column(db.String(100))
  candidate_name = db.Column(db.String(50))
  candidate_phone = db.Column(db.String(15))
  initial_scrape_complete = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CvInvalidFormatObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  invalid_file_type = db.Column(db.String(20))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class OpenAiQueueObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(50))
  question_type = db.Column(db.String(50))
  single_value = db.Column(db.String(150))
  multiple_values = db.Column(db.String(2000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class GradedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(50))
  fk_role_id = db.Column(db.String(150))
  fk_cv_id = db.Column(db.String(150))
  fk_role_name = db.Column(db.String(150))
  fk_cv_name = db.Column(db.String(50))
  summary = db.Column(db.String(2000))
  score = db.Column(db.Float)
  follow_ups = db.Column(db.String(2000))
  openai_response = db.Column(db.String(2000))
  fk_ref_key = db.Column(db.String(150))
  question_type = db.Column(db.String(50))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CvAskAiObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(50))
  fk_cv_id = db.Column(db.String(150))
  question = db.Column(db.String(200))
  answer = db.Column(db.String(2000))
  openai_response = db.Column(db.String(2000))
  fk_ref_key = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class FeedbackObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(50))
  message = db.Column(db.String(1000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class NotificationsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(50))
  topic = db.Column(db.String(50))
  message = db.Column(db.String(200))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class StripeCheckoutSessionObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(50))
  fk_checkout_session_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class StripePaymentOptionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  name = db.Column(db.String(20))
  price = db.Column(db.Float)
  fk_stripe_price_id = db.Column(db.String(150))
  fk_stripe_price_id_testing = db.Column(db.String(150))
  status = db.Column(db.String(50))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ConversionTrackingObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  event = db.Column(db.String(50))
  status = db.Column(db.String(50))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class BlogObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  title = db.Column(db.String(150))
  details = db.Column(db.String(150))
  keywords = db.Column(db.String(150))
  image_url = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=False)
  author_img_url = db.Column(db.String(150))
  author = db.Column(db.String(150))
  author_social_url = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class LinkedinScrapeObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  company = db.Column(db.String(150))
  role = db.Column(db.String(150))
  name = db.Column(db.String(150))
  subtitle = db.Column(db.String(150))
  url = db.Column(db.String(300))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CompanyInfoObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  name = db.Column(db.String(150))
  url = db.Column(db.String(150))
  active = db.Column(db.Boolean, default=True)
# ------------------------ individual model end ------------------------

"""
# ------------------------ individual model start ------------------------
class EmailCollectObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
  source = db.Column(db.String(20))
  unsubscribed = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------
# ------------------------ individual model start ------------------------
class EmailDeletedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), primary_key=True)
  uuid_archive = db.Column(db.String(150), primary_key=True)
# ------------------------ individual model end ------------------------
"""
