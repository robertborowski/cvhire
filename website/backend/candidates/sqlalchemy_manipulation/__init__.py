# ------------------------ imports start ------------------------

from website.backend.candidates.string_manipulation import string_to_arr_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def pull_desired_languages_arr_function(db_obj):
  output_arr = []
  for i_obj in db_obj:
    i_str = i_obj.desired_languages_str
    i_arr = string_to_arr_function(i_str)
    for i in i_arr:
      if i not in output_arr:
        output_arr.append(i)
  return output_arr
# ------------------------ individual function end ------------------------