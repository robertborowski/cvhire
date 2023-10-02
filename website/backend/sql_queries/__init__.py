# ------------------------ imports start ------------------------
import psycopg2.extras
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sql_general_function(postgres_cursor, query_name=None, var1=None, var2=None, var3=None):
  # ------------------------ set variables start ------------------------
  sql_query = ''
  queries_dict = {
    "latest_queue": f"SELECT * FROM {var1} WHERE status='requested' ORDER BY created_timestamp DESC;"
  }
  # ------------------------ set variables end ------------------------
  sql_query = queries_dict[query_name]
  postgres_cursor.execute(sql_query)
  results = postgres_cursor.fetchall()
  return results
# ------------------------ individual function end ------------------------
