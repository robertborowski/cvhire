# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ================================================ select start ================================================
# ------------------------ individual function start ------------------------
def sql_general_function(postgres_cursor, sql_query):
  postgres_cursor.execute(sql_query)
  results = postgres_cursor.fetchall()
  return results
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v1_function(postgres_cursor, var1=None):
  sql_query = f"SELECT * FROM open_ai_queue_obj WHERE status='{var1}' ORDER BY created_timestamp;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v2_function(postgres_cursor, var1=None, var2=None, var3=None):
  sql_query = f"SELECT * FROM {var1} WHERE id='{var2}' AND fk_user_id='{var3}' LIMIT 1;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v3_function(postgres_cursor, var1=None, var2=None, var3=None, var4=None):
  sql_query = f"SELECT * FROM {var1} WHERE fk_user_id='{var2}' and status='{var3}' and id IN ({var4});"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v4_function(postgres_cursor, var1=None, var2=None, var3=None):
  sql_query = f"SELECT * FROM {var1} WHERE fk_user_id='{var2}' and status='{var3}';"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v5_function(postgres_cursor, var1=None, var2=None, var3=None):
  sql_query = f"SELECT * FROM graded_obj WHERE fk_role_id='{var1}' and fk_cv_id='{var2}' and fk_user_id='{var3}' and status='valid';"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------
# ================================================ select end ================================================

# ================================================ insert start ================================================
# ------------------------ individual function start ------------------------
def insert_query_v1_function(postgres_connection, postgres_cursor, id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key, question_type):
  try:
    sql_query = "INSERT INTO graded_obj (id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key, question_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, summary, score, follow_ups, openai_response, fk_ref_key, question_type)
    postgres_cursor.execute(sql_query, data)
    postgres_connection.commit()
  except Exception as e:
    print(f'Error insert_query_v1_function: {e}')
    return False
  return True
# ------------------------ individual function end ------------------------
# ================================================ insert end ================================================

# ================================================ update start ================================================
# ------------------------ individual function start ------------------------
def update_query_v1_function(postgres_connection, postgres_cursor, var1=None, var2=None):
  try:
    sql_query = f"UPDATE open_ai_queue_obj SET status='{var1}' WHERE id='{var2}';"
    postgres_cursor.execute(sql_query)
    postgres_connection.commit()
  except:
    return False
  return True
# ------------------------ individual function end ------------------------
# ================================================ update end ================================================