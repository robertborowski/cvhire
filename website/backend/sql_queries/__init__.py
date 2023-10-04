# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sql_general_function(postgres_cursor, sql_query):
  postgres_cursor.execute(sql_query)
  results = postgres_cursor.fetchall()
  return results
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v1_function(postgres_cursor, var1=None, var2=None):
  sql_query = f"SELECT * FROM {var1} WHERE status='{var2}' ORDER BY created_timestamp;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v2_function(postgres_cursor, var1=None, var2=None):
  sql_query = f"SELECT * FROM {var1} WHERE id='{var2}' LIMIT 1;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v3_function(postgres_cursor, var1=None, var2=None, var3=None):
  sql_query = f"SELECT * FROM {var1} WHERE fk_user_id='{var2}' and status='active' and id IN ({var3});"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v4_function(postgres_cursor, var1=None, var2=None):
  sql_query = f"SELECT * FROM {var1} WHERE fk_user_id='{var2}' and status='active';"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def insert_query_v1_function(postgres_connection, postgres_cursor, id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key):
  try:
    sql_query = "INSERT INTO graded_obj (id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key)
    postgres_cursor.execute(sql_query, data)
    postgres_connection.commit()
  except Exception as e:
    print(f'Error insert_query_v1_function: {e}')
    return False
  return True
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
