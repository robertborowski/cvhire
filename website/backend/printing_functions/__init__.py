# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def print_x_emails_function(db_obj_all, input_limit):
  limit = int(input_limit)
  i_user = int(0)
  while i_user < limit:
    # ------------------------ print person start ------------------------
    db_obj = db_obj_all[i_user]
    # ------------------------ if not found start ------------------------
    if db_obj == None or db_obj == []:
      return False
    # ------------------------ if not found end ------------------------
    arr = db_obj.all_formats.split('~')
    print(f' ---------- person {str(i_user)} ---------- ')
    for i in arr:
      email = i + '@' + db_obj.website_address
      print(email)
    print(' ')
    # ------------------------ print person end ------------------------
    i_user += 1
  return True
# ------------------------ individual function end ------------------------
