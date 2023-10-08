# ------------------------ imports start ------------------------
import os, time
from os import path
import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import stripe
# ------------------------ imports end ------------------------

# ------------------------ define/initialize a new db sql_alchemy function start ------------------------
# what is SQLAlchemy: https://www.youtube.com/watch?v=6k6NxFyKKQo&ab_channel=Treehouse
# transfers data stored in a SQL database into python objects. (models.py file)
# Use python code to the read, create, delete, update the objects as well as the SQL database at the same time. 
# Instead of writing SQL scripts every step of the way.
# Result: No SQL is needed to create, maintain, and query the db! ORM: Object Relational Mapping 
# and you can connect it directly to Postgres
db = SQLAlchemy()
DB_NAME = os.environ.get('DATABASE_URL')
# ------------------------ define/initialize a new db sql_alchemy function end ------------------------

secret_key_ref = os.urandom(64)

# ------------------------ __init__ function start ------------------------
def create_app_function():
  # ------------------------ app setup start ------------------------
  # ------------------------ set timezone start ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ set timezone end ------------------------
  # ------------------------ create flask app start ------------------------
  # Flask constructor
  app = Flask(__name__)
  # To use a session, there has to be a secret key. The string should be something difficult to guess
  app.secret_key = secret_key_ref
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1) # This .replace was added because of an issue when pushing to heroku. Link: https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy 
  db.init_app(app)
  # ------------------------ create flask app end ------------------------
  # ------------------------ additional flask app configurations start ------------------------
  # Set session variables to perm so that user can remain signed in for x days
  app.permanent_session_lifetime = datetime.timedelta(days=30)
  # For removing cache from images for quiz questions. The URL was auto caching and not updating
  app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  app.config['UPLOAD_FOLDER'] = 'uploads'
  app.config['ALLOWED_EXTENSIONS'] = {'docx', 'pdf', 'txt'}
  app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024
  # ------------------------ additional flask app configurations end ------------------------
  # ------------------------ Handleing Error Messages START ------------------------
  @app.errorhandler(404) # inbuilt function which takes error as parameter
  def not_found(e):
    return render_template("exterior/error_404/index.html")
  # ------------------------ Handleing Error Messages END ------------------------
  # ------------------------ stripe api environment start ------------------------
  stripe.api_key = os.environ.get('STRIPE_API_KEY')  # PRODUCTION
  # stripe.api_key = os.environ.get('STRIPE_TEST_API_KEY')  # TESTING
  # ------------------------ stripe api environment end ------------------------
  # ------------------------ views/auths/routes imports start ------------------------
  from .cv_auth import cv_auth
  from .cv_views_admin import cv_views_admin
  from .cv_views_exterior import cv_views_exterior
  from .cv_views_interior import cv_views_interior
  from .cv_views_interior_ai import cv_views_interior_ai
  from .cv_views_interior_cv import cv_views_interior_cv
  from .cv_views_interior_roles import cv_views_interior_roles
  from .cv_views_interior_results import cv_views_interior_results
  from .cv_views_interior_export import cv_views_interior_export
  from .cv_views_interior_help import cv_views_interior_help
  from .cv_views_interior_notifications import cv_views_interior_notifications
  # ------------------------ views/auths/routes imports end ------------------------
  # ------------------------ views/auths/routes register blueprints start ------------------------
  app.register_blueprint(cv_auth, url_prefix='/')
  app.register_blueprint(cv_views_admin, url_prefix='/')
  app.register_blueprint(cv_views_exterior, url_prefix='/')
  app.register_blueprint(cv_views_interior, url_prefix='/')
  app.register_blueprint(cv_views_interior_ai, url_prefix='/')
  app.register_blueprint(cv_views_interior_cv, url_prefix='/')
  app.register_blueprint(cv_views_interior_roles, url_prefix='/')
  app.register_blueprint(cv_views_interior_results, url_prefix='/')
  app.register_blueprint(cv_views_interior_export, url_prefix='/')
  app.register_blueprint(cv_views_interior_help, url_prefix='/')
  app.register_blueprint(cv_views_interior_notifications, url_prefix='/')
  # ------------------------ views/auths/routes register blueprints end ------------------------
  # ------------------------ import models before creating db for first time start ------------------------
  from .models import UserObj
  create_database_function(app)
  # ------------------------ import models before creating db for first time end ------------------------
  # ------------------------ login manager start ------------------------
  login_manager = LoginManager()
  login_manager.login_view = 'cv_auth.cv_login_function'   # where does the person go if they are not logged in -> auth.login route
  login_manager.init_app(app)
  # ------------------------ function start ------------------------
  @login_manager.user_loader
  def load_user(id):
    return UserObj.query.get(id)  # when you write query.get -> .get: automatically knows it is looking through the primary key in sqlite
  # ------------------------ function end ------------------------
  # ------------------------ login manager end ------------------------
  # ------------------------ app setup end ------------------------
  return app
# ------------------------ __init__ function end ------------------------


# ------------------------ create_db_function start ------------------------
def create_database_function(app):
  """
  -Note: How to log everyone off. Remove all browser cookie keys from redis, THEN,
  you have to restart the app from heroku. restarting the main/index .py file will 
  log everyone off from flask login manager.
  """
  if not path.exists('website/' + DB_NAME):
    # ------------------------ old - editing model tables start ------------------------
    # db.create_all(app=app)
    # ------------------------ old - editing model tables end ------------------------
    # ------------------------ new - editing model tables start ------------------------
    # https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
    with app.app_context():
      db.create_all()
    # ------------------------ new - editing model tables end ------------------------
  else:
    pass
# ------------------------ create_db_function end ------------------------