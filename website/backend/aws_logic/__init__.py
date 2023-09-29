# ------------------------ imports start ------------------------
import boto3
import os
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
  return response
# ------------------------ individual function end ------------------------
