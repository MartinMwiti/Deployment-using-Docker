from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config


db = SQLAlchemy()  # sql alchemy database instance
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # the login_view we've passed i.e 'login' refers to function of our route. Same thing we would pass in the url_for() function.
# login_view-The name of the view to redirect to when the user needs to log in.
# login_view:this will be activated by the @login_required decorator in the account func found in the routes.py file.
login_manager.login_message_category = 'info'

mail = Mail() # initialize
# https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp


# flask will treat this as 'current_app'
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_blog.users.routes import users # put down instead of top to avoid circular imports problem. 'import users' is the instance of our blueprint route
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

















'''Reference: https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.login_view '''
