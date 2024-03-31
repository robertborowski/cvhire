# ------------------------ imports start ------------------------
import os
import datetime
import boto3
from botocore.exceptions import ClientError
from io import StringIO
import psycopg2
import pandas as pd
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
from website.backend.sql_queries import select_query_v8_function
from website.backend.sendgrid import send_email_template_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def run_function():
  # ------------------------ set variables start ------------------------
  # Get todays date as string
  todays_date_str = str(datetime.datetime.now().date())
  todays_date = todays_date_str.replace("-","")
  # ------------------------ set variables end ------------------------
  # ------------------------ open db start ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_open_function()
  # ------------------------ open db start ------------------------
  # ------------------------ get all ids as set start ------------------------
  cvs_set = {''}
  db_all_rows_arr = select_query_v8_function(postgres_cursor)
  for i in db_all_rows_arr:
    cvs_set.add(i[0])
  cvs_set.remove('')
  # ------------------------ get all ids as set end ------------------------
  # ------------------------ close connection start ------------------------
  # Close postgres db connection
  postgres_connect_close_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  # ------------------------ AWS Connect Bucket START ------------------------
  # Create AWS s3 client
  s3_resource = boto3.resource('s3')
  s3_bucket_name = os.environ.get('AWS_CVHIRE_BUCKET_NAME')
  # ------------------------ AWS Connect Bucket End ------------------------
  # ------------------------ get bucket objs start ------------------------
  bucket = s3_resource.Bucket(s3_bucket_name)
  for i_obj in bucket.objects.all():
    aws_file_name = i_obj.key
    if aws_file_name not in cvs_set:
      i_obj.delete()
  # ------------------------ get bucket objs end ------------------------
  # ------------------------ email self notifications start ------------------------
  try:
    output_to_email = os.environ.get('CVHIRE_SUPPORT_EMAIL')
    output_subject_self = f'job_daily: AWS cleanup CV bucket successful'
    output_body = f'job_daily_{todays_date}: AWS cleanup CV bucket successful'
    send_email_template_function(output_to_email, output_subject_self, output_body)
  except:
    pass
  # ------------------------ email self notifications end ------------------------
  return True
# ------------------------ individual function end ------------------------


# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------