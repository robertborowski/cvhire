# ------------------------ imports start ------------------------
from datetime import datetime
import os, time
import uuid
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def create_timestamp_function():
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_uuid_function(table_prefix):
  return table_prefix + str(uuid.uuid4())
# ------------------------ individual function end ------------------------