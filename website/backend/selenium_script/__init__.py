# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time
from website import db
import os
# ------------------------ imports end ------------------------

# ------------------------ scroll to bottom of the page start ------------------------
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# ------------------------ scroll to bottom of the page end ------------------------

# ------------------------ individual function start ------------------------
def linkedin_scraper_function(input1=None):
  # ------------------------ scraper #1 start ------------------------
  if input1 == 'normal':
    # ------------------------ webdriver open start ------------------------
    # ------------------------ incognito start ------------------------
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("start-maximized")
    # ------------------------ incognito end ------------------------
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.linkedin.com/')
    # ------------------------ webdriver open end ------------------------
    # ------------------------ set variables start ------------------------
    data_captured_dict = {}
    running_check = True
    run_count = -1
    company_names_arr = ['hellofresh']
    role_names_arr = ['recruiter']
    # ------------------------ set variables end ------------------------
    # ------------------------ recurring start ------------------------
    while running_check == True:
      run_count += 1
      # ------------------------ login start ------------------------
      login_function(driver)
      # ------------------------ login end ------------------------
      # ------------------------ search start ------------------------
      search_function(driver, company_names_arr[0], role_names_arr[0])
      # ------------------------ search end ------------------------
      # ------------------------ webdriver close start ------------------------
      driver.close()
      # ------------------------ webdriver close end ------------------------
      print(' ------------- 100 start ------------- ')
      data_captured_dict = dict(sorted(data_captured_dict.items(),key=lambda x:x[0]))
      for k,v in data_captured_dict.items():
        print(f"k: {k} | v: {v}")
        pass
      print(' ------------- 100 end ------------- ')
      return True
  # ------------------------ scraper #1 end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def random_int_function():
  return random.randint(2, 4)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def login_function(driver):
  # username
  element = driver.find_element(By.ID, 'session_key')
  element.click()
  element.send_keys(os.environ.get('LINKEDIN_USERNAME'))
  time.sleep(random_int_function())

  # password
  element = driver.find_element(By.ID, 'session_password')
  element.click()
  element.send_keys(os.environ.get('LINKEDIN_PASSWORD'))
  time.sleep(random_int_function())

  # sign in button
  element = driver.find_element(By.CSS_SELECTOR, '.sign-in-form__submit-btn--full-width')
  element.click()
  time.sleep(random_int_function())

  try:
    # email code
    element = driver.find_element(By.ID, 'input__email_verification_pin') 
    element.click()
    time.sleep(15)

    # submit button
    element = driver.find_element(By.ID, 'email-pin-submit-button')
    element.click()
    time.sleep(random_int_function())
  except:
    pass
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def search_function(driver, input_company_name, input_role_name):
  # search bar
  element = driver.find_element(By.CSS_SELECTOR, '.search-global-typeahead__input')
  element.click()
  element.send_keys(input_company_name + ' ' + input_role_name)
  element.send_keys(Keys.ENTER)
  time.sleep(random_int_function())

  # click "People" category of search
  element = driver.find_element(By.CSS_SELECTOR, '.search-reusables__filter-pill-button')
  element.click()
  time.sleep(random_int_function())
  return True
# ------------------------ individual function end ------------------------
