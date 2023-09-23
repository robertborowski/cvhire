# ------------------------ imports start ------------------------

from random import randint
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def string_to_arr_function(input_str):
  output_arr = []
  input_str_split_arr = input_str.split(',')
  for word in input_str_split_arr:
    word_stripped = word.strip()
    if word_stripped not in output_arr and word_stripped != 'Candidates' and word_stripped != 'MCQ':
      output_arr.append(word_stripped)
  return output_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def all_question_candidate_categories_sorted_function(query_result_arr_of_dicts):
  output_arr = []
  for i_dict in query_result_arr_of_dicts:
    categories_str = i_dict['categories']
    categories_arr = string_to_arr_function(categories_str)
    for i_category in categories_arr:
      if i_category not in output_arr:
        output_arr.append(i_category)
  output_arr = sorted(output_arr)
  return output_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def all_employee_question_categories_sorted_function(query_result_arr_of_dicts):
  output_arr = []
  for i_dict in query_result_arr_of_dicts:
    categories_str = i_dict['categories']
    categories_arr = string_to_arr_function(categories_str)
    for i_category in categories_arr:
      if i_category not in output_arr:
        output_arr.append(i_category)
  output_arr = sorted(output_arr)
  return output_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_assessment_name_function(ui_desired_languages_checkboxes_str):
  name_prefix = ui_desired_languages_checkboxes_str
  if len(ui_desired_languages_checkboxes_str) > 15:
    name_prefix = ui_desired_languages_checkboxes_str[0:15]
  name_suffix = randint(0, 9999)
  # ------------------------ special characters for HTML URL start ------------------------
  name_prefix = name_prefix.replace("#", "")
  # ------------------------ special characters for HTML URL end ------------------------
  return name_prefix + str(name_suffix)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def breakup_email_function(input_email):
  # print(' ------------------------ breakup_email_function start ------------------------ ')
  email_arr = input_email.split('@')
  try:
    email_arr = email_arr[0].split('.')
  except:
    pass
  # print(' ------------------------ breakup_email_function end ------------------------ ')
  return email_arr[0].lower().capitalize()
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def capitalize_all_words_function(input_str):
  capitalized_arr = []
  input_arr = input_str.split('_')
  for i in input_arr:
    i = i.capitalize()
    capitalized_arr.append(i)
  return ' '.join(capitalized_arr)
# ------------------------ individual function end ------------------------