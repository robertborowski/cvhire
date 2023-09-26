# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def convert_obj_row_to_dict_function(row):
  return {c.name: getattr(row, c.name) for c in row.__table__.columns}
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def objs_to_arr_of_dicts_function(db_obj, identifier=None):
  arr = []
  for i_obj in db_obj:
    i_dict = convert_obj_row_to_dict_function(i_obj)
    # ------------------------ additional details start ------------------------
    if identifier == 'roles':
      i_dict['name_display'] = i_dict['name'][:35]
    # ------------------------ additional details end ------------------------
    arr.append(i_dict)
  # ------------------------ return dict if only 1 start ------------------------
  if len(arr) == 1:
    return arr[0]
  # ------------------------ return dict if only 1 end ------------------------
  return arr
# ------------------------ individual function end ------------------------
