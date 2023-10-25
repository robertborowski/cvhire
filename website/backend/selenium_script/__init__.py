# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time
from website import db
import os
# ------------------------ imports end ------------------------

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
      # ------------------------ scrape info multiple pages start ------------------------
      data_captured_dict = multiple_pages_function(driver, data_captured_dict)
      # ------------------------ scrape info multiple pages end ------------------------
      # ------------------------ scraped info to db start ------------------------
      # ------------------------ scraped info to db end ------------------------
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

# ------------------------ individual function start ------------------------
def collect_function(driver, data_captured_dict):
  # ------------------------ all employee rows on page start ------------------------
  elements = driver.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')
  for i_element in elements:
    # ------------------------ employee name start ------------------------
    name_element = i_element.find_element(By.XPATH, ".//span[@dir='ltr']/span[1]")
    employee_display_name = name_element.text
    # ------------------------ employee name end ------------------------
    # ------------------------ employee company start ------------------------
    subtitle_element = i_element.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle")
    employee_display_subtitle = subtitle_element.text
    # ------------------------ employee company end ------------------------
    if employee_display_name not in data_captured_dict:
      data_captured_dict[employee_display_name] = employee_display_subtitle
  # ------------------------ all employee rows on page end ------------------------
  return data_captured_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def multiple_pages_function(driver, data_captured_dict):
  search_pages_max = 5
  current_page = 1
  while current_page < search_pages_max:
    try:
      # ------------------------ collect info start ------------------------
      data_captured_dict = collect_function(driver, data_captured_dict)
      # ------------------------ collect info end ------------------------
      # ------------------------ scroll to bottom of the page start ------------------------
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(random_int_function())
      # ------------------------ scroll to bottom of the page end ------------------------
      # ------------------------ click next page start ------------------------
      element = driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text()='Next']")
      element.click()
      time.sleep(random_int_function())
      # ------------------------ click next page end ------------------------
      # ------------------------ increase page counter start ------------------------
      current_page += 1
      # ------------------------ increase page counter end ------------------------
    except:
      # ------------------------ increase page counter start ------------------------
      current_page += 1
      # ------------------------ increase page counter end ------------------------
  return data_captured_dict
# ------------------------ individual function end ------------------------