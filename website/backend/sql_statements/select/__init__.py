# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import db
from flask_login import current_user
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def select_general_function(tag_query_to_use, input1=None, input2=None, input3=None, input4=None):
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_1': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      fk_show_id='{input1}' AND \
                      id NOT IN (SELECT fk_poll_id FROM polls_answered_obj WHERE fk_show_id='{input1}' AND fk_user_id='{input2}') \
                    ORDER BY \
                      RANDOM() \
                    LIMIT 1;"
    },
    'select_2': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      fk_show_id='{input1}' AND \
                      id='{input2}';"
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ general query start ------------------------
  result_obj = db.session.execute(select_queries_dict[tag_query_to_use]['raw_query'])
  # ------------------------ general query end ------------------------
  # ------------------------ existing result start ------------------------
  result_arr_of_dicts = []
  for i_row in result_obj:
    result_dict = dict(i_row) # convert to dict keyed by column names
    result_arr_of_dicts.append(result_dict)
  # ------------------------ existing result end ------------------------
  return result_arr_of_dicts
# ------------------------ individual function end ------------------------