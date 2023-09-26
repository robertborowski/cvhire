# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def convert_obj_row_to_dict_function(row):
  return {c.name: getattr(row, c.name) for c in row.__table__.columns}
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def objs_to_arr_of_dicts_function(db_obj):
  arr = []
  for i_obj in db_obj:
    arr.append(convert_obj_row_to_dict_function(i_obj))
  return arr
# ------------------------ individual function end ------------------------
