# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.backend.connection import redis_connect_open_function
from website.models import BlogObj
from website import db
from website.backend.alerts import get_alert_message_function
from website.backend.convert import objs_to_arr_of_dicts_function
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
@cv_views_blog.route('/blog/<url_redirect_code>')
@cv_views_blog.route('/blog/<url_redirect_code>/')
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
  # ------------------------ set variables end ------------------------
  # ------------------------ get all blog posts from db start ------------------------
  db_objs = BlogObj.query.filter_by(status=True).order_by(BlogObj.created_timestamp.desc()).all()
  # ------------------------ get all blog posts from db end ------------------------
  # ------------------------ convert objs to dict start ------------------------
  page_dict['db_arr_dicts'] = objs_to_arr_of_dicts_function(db_objs, 'blog')
  # ------------------------ convert objs to dict end ------------------------
  return render_template('exterior/blog/index.html', page_dict_html=page_dict)
# ------------------------ individual route end ------------------------
