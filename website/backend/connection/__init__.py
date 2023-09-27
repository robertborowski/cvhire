# ------------------------ imports start ------------------------
import psycopg2
from psycopg2 import Error
import os
import redis
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def postgres_connect_open_function():
  # Heroku Postgres connection
  DATABASE_URL = os.environ.get('DATABASE_URL')
  postgres_connection = psycopg2.connect(DATABASE_URL, sslmode='require')
  postgres_cursor = postgres_connection.cursor()
  return postgres_connection, postgres_cursor
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def postgres_connect_close_function(postgres_connection, postgres_cursor):
  postgres_cursor.close()
  postgres_connection.close()
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def redis_connect_open_function():
  try:
    # Connecting to Redis pool method
    pool = redis.ConnectionPool(
      host = os.environ.get('CVHIRE_REDIS_HOST_NAME'),
      port = str(os.environ.get('CVHIRE_REDIS_PORT')),
      password = os.environ.get('CVHIRE_REDIS_PASSWORD'),
      db=0)
    #redis_connection = redis.Redis(connection_pool=pool)
    redis_connection = redis.StrictRedis(connection_pool=pool)
  
  except:
    return 'redis connection failed!'
    
  # Return the connection
  return redis_connection
# ------------------------ individual function end ------------------------