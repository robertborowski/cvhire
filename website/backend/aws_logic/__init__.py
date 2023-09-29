# ------------------------ imports start ------------------------
import boto3
import os
from website import db
from website.models import CvObj
from website.backend.read_files import get_file_contents_function
from website.backend.open_ai_chatgpt import get_name_and_email_from_cv_function
from website.backend.uploads_user import get_file_suffix_function
from io import BytesIO
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def upload_file_to_aws_s3_function(file_to_upload, aws_file_name):
  S3_BUCKET_NAME = os.environ.get('AWS_CVHIRE_BUCKET_NAME')
  s3 = boto3.client('s3')
  s3.upload_fileobj(file_to_upload, S3_BUCKET_NAME, aws_file_name)
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_file_from_aws_function(file_path):
  s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
  bucket_name = os.environ.get('AWS_CVHIRE_BUCKET_NAME')
  response = s3.get_object(Bucket=bucket_name, Key=file_path)
  return BytesIO(response['Body'].read())
# ------------------------ individual function end ------------------------

# ------------------------ individual route start ------------------------
def initial_cv_scrape_function(id_current_user):
  # This function is here because on uploading cv's to aws s3, s3 automatically 'closes' the file upon upload and that doesn't let me scrape the file. If I try to scrape the file first then upload to aws then the file gets corrupted.
  db_objs = CvObj.query.filter_by(fk_user_id=id_current_user,initial_scrape_complete=False).all()
  # ------------------------ if none start ------------------------
  if db_objs == None or db_objs == []:
    return False
  # ------------------------ if none end ------------------------
  # ------------------------ loop through each row start ------------------------
  for i_obj in db_objs:
    i_file_aws = get_file_from_aws_function(i_obj.cv_aws_id)
    # ------------------------ get file suffix start ------------------------
    file_format_suffix = get_file_suffix_function(i_obj.cv_aws_id)
    # ------------------------ get file suffix end ------------------------
    # ------------------------ read file contents start ------------------------
    cv_contents = get_file_contents_function(i_file_aws, file_format_suffix)
    # ------------------------ read file contents end ------------------------
    # ------------------------ read candidate name and email from contents start ------------------------
    cv_name, cv_email, cv_phone = get_name_and_email_from_cv_function(cv_contents)
    # ------------------------ read candidate name and email from contents end ------------------------
    # ------------------------ update db start ------------------------
    i_obj.initial_scrape_complete = True
    if cv_name != None or cv_email != None or cv_phone != None:
      i_obj.candidate_name = cv_name
      i_obj.candidate_email = cv_email
      i_obj.candidate_phone = cv_phone
    db.session.commit()
    # ------------------------ update db end ------------------------
  # ------------------------ loop through each row end ------------------------
  return True
# ------------------------ individual route end ------------------------