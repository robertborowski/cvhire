# -------------------------------------------------------------- Imports
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.get_upcoming_week_dates_data_dict import get_upcoming_week_dates_data_dict_function
from datetime import date, datetime
from backend.utils.datetime_utils.quiz_due_time_convert_dict import quiz_due_time_convert_dict_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def check_if_today_is_greater_than_equal_to_latest_quiz_end_date_function(quiz_end_day_of_week, quiz_end_time):
  localhost_print_function('=========================================== check_if_today_is_greater_than_equal_to_latest_quiz_end_date_function START ===========================================')


  # ------------------------ This Week Dates Data Dict START ------------------------
  this_upcoming_week_dates_dict = get_upcoming_week_dates_data_dict_function()
  # ------------------------ This Week Dates Data Dict END ------------------------


  # ------------------------ Get Today's Date and Time START ------------------------
  # Today's date
  today_date = date.today()
  # Current Time
  current_time = datetime.now().strftime("%H:%M:%S")                  # str
  current_hour_int = int(current_time[0:2])                           # int
  # ------------------------ Get Today's Date and Time END ------------------------


  # ------------------------ Quiz Variables START ------------------------
  quiz_official_end_date = datetime.strptime(this_upcoming_week_dates_dict[quiz_end_day_of_week], '%Y-%m-%d').date()

  quiz_time_convert_dict = quiz_due_time_convert_dict_function()
  quiz_end_time_comparison = quiz_time_convert_dict[quiz_end_time]    # str
  quiz_end_time_comparison_int = int(quiz_end_time_comparison[0:2])   # int
  # ------------------------ Quiz Variables END ------------------------


  # ------------------------ Check If Today Is Earlier Than Latest Quiz Start Date START ------------------------
  if today_date > quiz_official_end_date:
    localhost_print_function('=========================================== check_if_today_is_greater_than_equal_to_latest_quiz_end_date_function END ===========================================')
    return True
  
  if today_date == quiz_official_end_date:
    if current_hour_int >= quiz_end_time_comparison_int:
      localhost_print_function('=========================================== check_if_today_is_greater_than_equal_to_latest_quiz_end_date_function END ===========================================')
      return True
    else:
      localhost_print_function('today is equal to quiz end date but current time is less than quiz end time')
      localhost_print_function('=========================================== check_if_today_is_greater_than_equal_to_latest_quiz_end_date_function END ===========================================')
      return False
  
  else:
    localhost_print_function('today is not equal to quiz end date')
    localhost_print_function('=========================================== check_if_today_is_greater_than_equal_to_latest_quiz_end_date_function END ===========================================')
    return False
  # ------------------------ Check If Today Is Earlier Than Latest Quiz Start Date END ------------------------