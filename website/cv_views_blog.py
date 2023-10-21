# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.backend.connection import redis_connect_open_function
from website.models import UserObj, EmailSentObj
from website import db
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
def blog_function():
  return render_template('exterior/reset/index.html')
# ------------------------ individual route end ------------------------
