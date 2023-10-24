# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from website import db
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
    driver.get('https://www.reddit.com/user/smile-thank-you/submitted/')
    # ------------------------ webdriver open end ------------------------
    """
    # ------------------------ set variables start ------------------------
    data_captured_dict = {}
    running_check = True
    run_count = -1
    # ------------------------ set variables end ------------------------
    # ------------------------ recurring start ------------------------
    while running_check == True:
      run_count += 1
      # ------------------------ scroll to bottom of the page start ------------------------
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      # ------------------------ scroll to bottom of the page end ------------------------
      # ------------------------ get lists/variables start ------------------------
      element_all_posts_arr = driver.find_elements(By.CSS_SELECTOR,'[view-type="cardView"]') # type: list
      # ------------------------ get lists/variables end ------------------------
      for i_post in range(len(element_all_posts_arr)): # type: <class 'selenium.webdriver.remote.webelement.WebElement'>
        # ------------------------ check in/add to dict start ------------------------
        if element_all_posts_arr[i_post] in data_captured_dict:
          continue
        if i_post not in data_captured_dict:
          data_captured_dict[element_all_posts_arr[i_post]] = {}
        # ------------------------ check in/add to dict end ------------------------
        # ------------------------ pull/assign variables start ------------------------
        data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_posted_time_ago'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_title'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_votes'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_comments'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_url'] = get_general_info_function(element_all_posts_arr, i_post)
        # ------------------------ pull/assign variables end ------------------------
        # ------------------------ cutooff check start ------------------------
        if 'days ago' in data_captured_dict[element_all_posts_arr[i_post]]['reddit_posted_time_ago']:
          num_days = int(data_captured_dict[element_all_posts_arr[i_post]]['reddit_posted_time_ago'].replace(' days ago', ''))
          if num_days >= 20:
            running_check = False
            break
        # ------------------------ cutooff check end ------------------------
        # ------------------------ pull/create reddit post from db start ------------------------
        db_reddit_post_obj = pull_create_update_reddit_post_function(data_captured_dict, element_all_posts_arr, i_post)
        # ------------------------ pull/create reddit post from db end ------------------------
        # ------------------------ new commentary check start ------------------------
        new_commentary_db_check = False
        db_comments_obj = RedditCommentsObj.query.filter_by(fk_reddit_post_id=db_reddit_post_obj.id).all()
        if len(db_comments_obj) < (int(db_reddit_post_obj.total_comments) - int(db_reddit_post_obj.total_replies)):
          new_commentary_db_check = True
        # ------------------------ new commentary check end ------------------------
        # ------------------------ get new comments start ------------------------
        if new_commentary_db_check == True:
          driver.get(data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_url'])
          data_captured_dict = get_all_comments_from_post_function(data_captured_dict, element_all_posts_arr, i_post, driver)
          # ------------------------ collect all comments from post end ------------------------
          # ------------------------ add to db start ------------------------
          add_commentary_to_db_function(data_captured_dict, element_all_posts_arr, i_post, db_reddit_post_obj)
          # ------------------------ add to db end ------------------------
          driver.get('https://www.reddit.com/user/smile-thank-you/submitted/')
          time.sleep(3)
          break
        # ------------------------ get new comments end ------------------------
    # ------------------------ recurring end ------------------------
    """
    # ------------------------ webdriver close start ------------------------
    driver.close()
    # ------------------------ webdriver close end ------------------------
  # ------------------------ scraper #1 end ------------------------
  return True
# ------------------------ individual function end ------------------------
