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

# ------------------------ individual function start ------------------------
def select_query_v6_function(postgres_cursor, var1=None):
  sql_query = f"SELECT id,created_timestamp,fk_user_id,status,fk_role_id,fk_cv_id,fk_role_name,fk_cv_name,summary,score,follow_ups FROM graded_obj WHERE fk_user_id='{var1}' and status!='delete' ORDER BY created_timestamp;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v7_function(postgres_cursor, var1=None):
  sql_query = f"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def select_query_v8_function(postgres_cursor, var1=None):
  sql_query = f"SELECT cv_aws_id FROM cv_obj;"
  return sql_general_function(postgres_cursor, sql_query)
# ------------------------ individual function end ------------------------
# ================================================ select end ================================================

# ================================================ insert start ================================================
# ------------------------ individual function start ------------------------
def insert_query_v1_function(postgres_connection, postgres_cursor, id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, fk_role_name, fk_cv_name, summary, score, follow_ups, openai_response, fk_ref_key, question_type):
  try:
    sql_query = "INSERT INTO graded_obj (id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, fk_role_name, fk_cv_name, summary, score, follow_ups, openai_response, fk_ref_key, question_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (id, created_timestamp, fk_user_id, status, fk_role_id, fk_cv_id, fk_role_name, fk_cv_name, summary, score, follow_ups, openai_response, fk_ref_key, question_type)
    postgres_cursor.execute(sql_query, data)
    postgres_connection.commit()
  except Exception as e:
    print(f'Error insert_query_v1_function: {e}')
    return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def insert_query_v2_function(postgres_connection, postgres_cursor, id, created_timestamp, fk_user_id, status, fk_cv_id, question, answer, openai_response, fk_ref_key):
  try:
    sql_query = "INSERT INTO cv_ask_ai_obj (id, created_timestamp, fk_user_id, status, fk_cv_id, question, answer, openai_response, fk_ref_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (id, created_timestamp, fk_user_id, status, fk_cv_id, question, answer, openai_response, fk_ref_key)
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
def update_query_v1_function(postgres_connection, postgres_cursor, var1=None, var2=None, var3=None):
  try:
    sql_query = f"UPDATE {var3} SET status='{var1}' WHERE id='{var2}';"
    postgres_cursor.execute(sql_query)
    postgres_connection.commit()
  except:
    return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def update_query_v2_function(postgres_connection, postgres_cursor, var1=None, var2=None):
  try:
    sql_query = f"UPDATE email_scraped_obj SET correct_format='{var1}' WHERE website_address='{var2}';"
    postgres_cursor.execute(sql_query)
    postgres_connection.commit()
  except:
    return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def update_query_v3_function(postgres_connection, postgres_cursor):
  try:
    sql_query = f"UPDATE company_info_obj SET active=False WHERE active=True;"
    postgres_cursor.execute(sql_query)
    postgres_connection.commit()
  except:
    return False
  return True
# ------------------------ individual function end ------------------------
# ================================================ update end ================================================