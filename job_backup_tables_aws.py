# ------------------------ imports start ------------------------
import os
import datetime
import boto3
from botocore.exceptions import ClientError
from io import StringIO
import psycopg2
import pandas as pd
from website.backend.connection import postgres_connect_open_function, postgres_connect_close_function
from website.backend.sql_queries import select_query_v7_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def run_function():
  # ------------------------ AWS Connect Bucket START ------------------------
  # Create AWS s3 client
  s3_resource = boto3.resource('s3')
  s3_bucket_name = os.environ.get('CVHIRE_BACKUP_BUCKET')
  # ------------------------ AWS Connect Bucket End ------------------------
  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_open_function()
  # ------------------------ DB Conection End ------------------------
  # ------------------------ SQL Get DB Table Names START ------------------------
  # Get all table names in the current database
  db_table_names_arr = select_query_v7_function(postgres_cursor)
  # ------------------------ SQL Get DB Table Names END ------------------------
  # ------------------------ Push Info Into AWS s3 START ------------------------
  for table_name_arr in db_table_names_arr:
    # Get table name
    table_name = table_name_arr[0]
    try:
      # ------------------------ Get Individual Table Data START ------------------------
      # Run sql statement on the table and get all row results
      postgres_cursor.execute("SELECT * FROM %s" % table_name)
      result_list = postgres_cursor.fetchall()
      # ------------------------ Get Individual Table Data END ------------------------
      # ------------------------ Get Individual Table Headers START ------------------------
      # Get table headers, store in array
      headers_tuple = postgres_cursor.description
      headers_arr = []
      for i in headers_tuple:
        headers_arr.append(i.name)
      # ------------------------ Get Individual Table Headers END ------------------------
      # Create into pandas dataframe
      df = pd.DataFrame(result_list, columns=headers_arr)
      # Get todays date as string
      todays_date_str = str(datetime.datetime.now().date())
      todays_date = todays_date_str.replace("-","")
      # ------------------------ Upload to AWS s3 as csv START ------------------------
      # Upload pandas df into aws s3
      csv_buffer = StringIO()
      df.to_csv(csv_buffer)
      s3_resource.Object(s3_bucket_name, todays_date + '_' + table_name + '.csv').put(Body=csv_buffer.getvalue())
      # ------------------------ Upload to AWS s3 as csv END ------------------------
    # Except clause
    except (Exception, psycopg2.Error) as error:
      print('error')
      postgres_connect_close_function(postgres_connection, postgres_cursor)
      return False
  # ------------------------ Push Info Into AWS s3 END ------------------------
  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_connect_close_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------
  return True
# ------------------------ individual function end ------------------------


# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------