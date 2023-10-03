# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sql_general_function(postgres_cursor, sql_query):
  postgres_cursor.execute(sql_query)
  results = postgres_cursor.fetchall()
  return results
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v1_function(postgres_cursor, var1=None):
  sql_query = f"SELECT * FROM {var1} WHERE status='requested' ORDER BY created_timestamp DESC;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v2_function(postgres_cursor, var1=None, var2=None):
  sql_query = f"SELECT * FROM {var1} WHERE id='{var2}' LIMIT 1;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v3_function(postgres_cursor, var1=None, var2=None):
  sql_query = f"SELECT * FROM {var1} WHERE id IN ({var2});"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v4_function(postgres_cursor, var1=None, var2=None):
  sql_query = f"SELECT * FROM {var1} WHERE fk_user_id='{var2}';"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def update_query_v1_function(postgres_connection, postgres_cursor, var1=None, var2=None, var3=None):
  try:
    sql_query = f"UPDATE {var1} SET {var2}='{var3}';"
    postgres_cursor.execute(sql_query)
    postgres_connection.commit()
  except:
    return False
  return True
# ------------------------ individual function end ------------------------
