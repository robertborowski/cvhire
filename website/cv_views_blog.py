# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.backend.connection import redis_connect_open_function
from website.models import BlogObj
from website import db
from website.backend.alerts import get_alert_message_function
from website.backend.convert import objs_to_arr_of_dicts_function, convert_obj_row_to_dict_function
from website.backend.convert import present_title_function, keywords_present_function, timestamp_to_date_function
from website.backend.static_lists import navbar_link_dict_exterior_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
cv_views_blog = Blueprint('cv_views_blog', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_open_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_blog.route('/blog')
@cv_views_blog.route('/blog/')
def blog_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = get_alert_message_function(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = True
  page_dict['category_specific'] = False
  page_dict['is_blog_page'] = True
  # ------------------------ set variables end ------------------------
  # ------------------------ get all blog posts from db start ------------------------
  db_objs = BlogObj.query.filter_by(status=True).order_by(BlogObj.created_timestamp.desc()).all()
  # ------------------------ get all blog posts from db end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  return render_template('exterior/blog/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_blog.route('/blog/category')
@cv_views_blog.route('/blog/category/')
@cv_views_blog.route('/blog/category/<url_category_code>')
@cv_views_blog.route('/blog/category/<url_category_code>/')
@cv_views_blog.route('/blog/category/<url_category_code>/<url_redirect_code>')
@cv_views_blog.route('/blog/category/<url_category_code>/<url_redirect_code>/')
def blog_category_function(url_category_code=None, url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = get_alert_message_function(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ page dict start ------------------------
  if url_category_code == None:
    try:
      url_category_code = request.args.get('url_category_code')
    except:
      pass
  # ------------------------ page dict end ------------------------
  # ------------------------ fix variable start ------------------------
  try:
    url_category_code = url_category_code.replace('-',' ')
  except:
    pass
  # ------------------------ fix variable end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = True
  page_dict['category_specific'] = True
  page_dict['category_title'] = present_title_function(url_category_code)
  # ------------------------ set variables end ------------------------
  # ------------------------ get all blog posts from db start ------------------------
  db_objs = BlogObj.query.filter_by(status=True).filter(BlogObj.keywords.like(f'%{url_category_code}%')).order_by(BlogObj.created_timestamp.desc()).all()
  # ------------------------ get all blog posts from db end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  return render_template('exterior/blog/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@cv_views_blog.route('/blog/<url_blog_code>')
@cv_views_blog.route('/blog/<url_blog_code>/')
@cv_views_blog.route('/blog/<url_blog_code>/<url_redirect_code>')
@cv_views_blog.route('/blog/<url_blog_code>/<url_redirect_code>/')
def blog_post_function(url_blog_code=None, url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = get_alert_message_function(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ page dict start ------------------------
  if url_blog_code == None:
    try:
      url_blog_code = request.args.get('url_blog_code')
    except:
      pass
  # ------------------------ page dict end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['nav_header'] = True
  # ------------------------ set variables end ------------------------
  # ------------------------ get all blog posts from db start ------------------------
  db_obj = BlogObj.query.filter_by(slug=url_blog_code).order_by(BlogObj.created_timestamp.desc()).first()
  # ------------------------ get all blog posts from db end ------------------------
  # ------------------------ not found redirect start ------------------------
  if db_obj == None or db_obj == []:
    return redirect(url_for('cv_views_blog.blog_function', url_redirect_code='e10'))
  # ------------------------ not found redirect end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['blog_dict'] = convert_obj_row_to_dict_function(db_obj)
  page_dict['blog_dict']['keywords_read_dict'] = keywords_present_function(page_dict['blog_dict']['keywords'])
  page_dict['blog_dict']['created_timestamp_read'] = timestamp_to_date_function(page_dict['blog_dict']['created_timestamp'])
  # ------------------------ convert objs to dict end ------------------------
  # ------------------------ get blog post number start ------------------------
  blog_post_arr = db_obj.id.split('_')
  blog_post_num = int(blog_post_arr[-1])
  html_template = f'exterior/blog/i_blog/post{ blog_post_num }.html'
  # ------------------------ get blog post number end ------------------------
  # ------------------------ get navbar variables start ------------------------
  page_dict['navbar_dict'] = navbar_link_dict_exterior_function()
  # ------------------------ get navbar variables end ------------------------
  return render_template(html_template, page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
