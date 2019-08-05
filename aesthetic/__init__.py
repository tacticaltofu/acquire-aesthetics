from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.markdown import Markdown
from aesthetic.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	app.jinja_env.globals.update(count=len)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	Markdown(app)

	from aesthetic.users.routes import users
	from aesthetic.posts.routes import posts
	from aesthetic.main.routes import main
	from aesthetic.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app