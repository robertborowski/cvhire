# ------------------------ imports start ------------------------

import random
import string
# ------------------------ imports end ------------------------


# ------------------------ individual function start ------------------------
def generate_random_length_uuid_function(num_characters):
  # print(' ------------------------ generate_random_length_uuid_function start ------------------------')
  generated_value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_characters))
  # print(' ------------------------ generate_random_length_uuid_function end ------------------------')
  return generated_value
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def question_choices_function():
  quiz_cadence_arr = ['Weekly', 'Biweekly', 'Monthly']
  question_num_arr = [5,10]
  question_type_arr = ['Multiple choice','Fill in the blank','Mixed']
  return quiz_cadence_arr, question_num_arr, question_type_arr
# ------------------------ individual function end ------------------------