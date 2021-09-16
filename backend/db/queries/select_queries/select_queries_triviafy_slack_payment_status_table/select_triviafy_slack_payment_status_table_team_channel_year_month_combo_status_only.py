# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function(postgres_connection, postgres_cursor, slack_team_id, slack_channel_id, payment_status_year, payment_status_month):
  localhost_print_function('=========================================== select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT payment_status_final_paid_customer FROM triviafy_slack_payment_status_table WHERE payment_status_slack_team_id=%s AND payment_status_slack_channel_id=%s AND payment_status_year=%s AND payment_status_month=%s", [slack_team_id, slack_channel_id, payment_status_year, payment_status_month])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function END ===========================================')
      return None