# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def convert_obj_row_to_dict_function(row):
  return {c.name: getattr(row, c.name) for c in row.__table__.columns}
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def objs_to_arr_of_dicts_function(db_obj, identifier=None):
  arr = []
  # ------------------------ variables for radios and checkboxes start ------------------------
  i_counter = 0
  # ------------------------ variables for radios and checkboxes end ------------------------
  for i_obj in db_obj:
    # ------------------------ variables for radios and checkboxes start ------------------------
    i_counter += 1
    # ------------------------ variables for radios and checkboxes end ------------------------
    i_dict = convert_obj_row_to_dict_function(i_obj)
    # ------------------------ additional details start ------------------------
    if identifier == 'roles':
      char_limit = 35
      i_dict['name_display'] = i_dict['name'][:char_limit]
      # ------------------------ variables for radios and checkboxes start ------------------------
      i_dict['radio_count_id'] = 'radio_count_' + str(i_counter)
      # ------------------------ variables for radios and checkboxes end ------------------------
    # ------------------------ additional details end ------------------------
    # ------------------------ additional details start ------------------------
    if identifier == 'cv':
      # ------------------------ variables for radios and checkboxes start ------------------------
      i_dict['checkbox_count_id'] = 'checkbox_count_' + str(i_counter)
      # ------------------------ variables for radios and checkboxes end ------------------------
      char_limit = 30
      i_dict['cv_upload_name_display'] = i_dict['cv_upload_name'][:char_limit]
      try:
        i_dict['candidate_email_display'] = i_dict['candidate_email'][:char_limit]
      except:
        pass
      try:
        i_dict['candidate_name_display'] = i_dict['candidate_name'][:char_limit]
      except:
        pass
      try:
        i_dict['candidate_phone_display'] = i_dict['candidate_phone'][:char_limit]
      except:
        pass
    # ------------------------ additional details end ------------------------
    arr.append(i_dict)
  return arr
# ------------------------ individual function end ------------------------
