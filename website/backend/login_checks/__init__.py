# ------------------------ imports start ------------------------

# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def product_login_checks_function(current_user, desired_product):
  is_match = False
  if current_user.signup_product == desired_product:
    is_match = True
  return is_match
# ------------------------ individual function end ------------------------