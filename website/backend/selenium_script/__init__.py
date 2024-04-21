# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from website import db
from website.models import LinkedinScrapeObj
import os
from website.backend.uuid_timestamp import create_uuid_function, create_timestamp_function
from website.backend.static_lists import get_all_companies_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def linkedin_scraper_function():
  # ------------------------ webdriver open start ------------------------
  # ------------------------ incognito start ------------------------
  options = webdriver.ChromeOptions()
  options.add_argument("--incognito")
  options.add_argument("start-maximized")
  # ------------------------ incognito end ------------------------
  driver = webdriver.Chrome(options=options)
  driver.get('https://www.linkedin.com/')
  # ------------------------ webdriver open end ------------------------
  # ------------------------ login start ------------------------
  login_function(driver)
  # ------------------------ login end ------------------------
  # ------------------------ set variables start ------------------------
  company_names_arr = get_all_companies_function()
  role_names_arr = ['recruiter','talent acquisition']
  # ------------------------ set variables end ------------------------
  # ------------------------ recurring start ------------------------
  for i_company in company_names_arr:
    for i_role in role_names_arr:
      # ------------------------ set variables start ------------------------
      data_captured_dict = {}
      # ------------------------ set variables end ------------------------
      # ------------------------ search start ------------------------
      search_function(driver, i_company, i_role)
      # ------------------------ search end ------------------------
      # ------------------------ scrape info multiple pages start ------------------------
      data_captured_dict = multiple_pages_function(driver, data_captured_dict)
      # ------------------------ scrape info multiple pages end ------------------------
      # ------------------------ scraped info to db start ------------------------
      upload_to_db_function(data_captured_dict, i_company, i_role)
      # ------------------------ scraped info to db end ------------------------
  # ------------------------ webdriver close start ------------------------
  driver.close()
  # ------------------------ webdriver close end ------------------------
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
  time.sleep(random_int_function())

  # delete previous
  actions = ActionChains(driver)
  actions.key_down(Keys.COMMAND).send_keys('a').perform()
  actions.key_up(Keys.COMMAND).perform()
  element.send_keys(Keys.DELETE)
  time.sleep(random_int_function())
  
  # search typing
  element.send_keys(input_company_name + ' ' + input_role_name)
  time.sleep(random_int_function())
  element.send_keys(Keys.ENTER)
  time.sleep(random_int_function())

  # click "People" category of search
  current_url = driver.current_url
  if 'people' not in current_url:
    time.sleep(random_int_function())
    elements = driver.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-pill-button')
    for i_element in elements:
      if i_element.text.lower() == 'people':
        i_element.click()
    time.sleep(random_int_function())

  # click and fill out "Current company" filter
  if 'currentCompany' not in current_url:
    # Click filter
    element = driver.find_element(By.ID, 'searchFilter_currentCompany') 
    element.click()
    time.sleep(random_int_function())
    # Click search bar
    element = driver.find_element(By.XPATH, "//input[@aria-label='Add a company']")
    element.click()
    time.sleep(random_int_function())
    # Search
    element.send_keys(input_company_name)
    time.sleep(random_int_function())
    # Arrow keys to select first option
    element.send_keys(Keys.DOWN)
    time.sleep(random_int_function())
    element.send_keys(Keys.ENTER)
    time.sleep(random_int_function())
    # Submit filter search
    elements = driver.find_elements(By.CSS_SELECTOR, 'button[data-test-reusables-filter-apply-button="true"]')
    for i_element in elements:
      span = i_element.find_element(By.CLASS_NAME, "artdeco-button__text")
      if span.text.lower() == 'show results':
        span.click()
        time.sleep(random_int_function())

  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def collect_function(driver, data_captured_dict):
  # ------------------------ all employee rows on page start ------------------------
  elements = driver.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')
  for i_element in elements:
    try:
      # ------------------------ employee name start ------------------------
      name_element = i_element.find_element(By.XPATH, ".//span[@dir='ltr']/span[1]")
      employee_display_name = name_element.text
      # ------------------------ employee name end ------------------------
      # ------------------------ employee company start ------------------------
      subtitle_element = i_element.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle")
      employee_display_subtitle = subtitle_element.text
      # ------------------------ employee company end ------------------------
      # ------------------------ employee url start ------------------------
      url_element = i_element.find_elements(By.CSS_SELECTOR, ".app-aware-link")
      employee_url = url_element[0].get_attribute('href')
      # ------------------------ employee url end ------------------------
      # ------------------------ add to dict start ------------------------
      if employee_display_name not in data_captured_dict:
        data_captured_dict[employee_display_name] = {}
        data_captured_dict[employee_display_name]['subtitle'] = employee_display_subtitle
        data_captured_dict[employee_display_name]['url'] = employee_url
      # ------------------------ add to dict end ------------------------
    except Exception as e:
      print(f'Exception collect_function: {e}')
  # ------------------------ all employee rows on page end ------------------------
  return data_captured_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def multiple_pages_function(driver, data_captured_dict):
  search_pages_max = 10
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
    except Exception as e:
      # ------------------------ increase page counter start ------------------------
      print(f'Exception multiple_pages_function: {e}')
      current_page += 1
      # ------------------------ increase page counter end ------------------------
  return data_captured_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def upload_to_db_function(data_captured_dict, searched_company_name, searched_role_name):
  for k,v in data_captured_dict.items():
    db_obj = LinkedinScrapeObj.query.filter_by(name=k,company=searched_company_name).first()
    if db_obj == None or db_obj == []:
      # ------------------------ force cutoff start ------------------------
      if len(k) > 150:
        k = k[0:149]
      if len(v['subtitle']) > 150:
        v['subtitle'] = v['subtitle'][0:149]
      # ------------------------ force cutoff end ------------------------
      # ------------------------ new row start ------------------------
      try:
        new_row = LinkedinScrapeObj(
          id=create_uuid_function('role_'),
          created_timestamp=create_timestamp_function(),
          company=searched_company_name,
          role=searched_role_name,
          name=k,
          subtitle=v['subtitle'],
          url=v['url']
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ new row end ------------------------
  return True
# ------------------------ individual function end ------------------------
