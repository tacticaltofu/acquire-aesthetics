import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.markdown import Markdown
from aesthetic.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	app.jinja_env.globals.update(count=len)

	db.init_app(app)
	migrate.init_app(app, db)
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

	if not app.debug and not app.testing:
		if app.config['LOG_TO_STDOUT']:
			stream_handler = logging.StreamHandler()
			stream_handler.setLevel(logging.INFO)
			app.logger.addHandler(stream_handler)
		else:
			if not os.path.exists('logs'):
				os.mkdir('logs')
			file_handler = RotatingFileHandler('logs/aesthetic.log', maxBytes=10240, backupCount=10)
			file_handler.setFormatter(logging.Formatter(
				'%(asctime)s %(levelname)s: %(message)s '
				'[in %(pathname)s:%(lineno)d]'))
			file_handler.setLevel(logging.INFO)
			app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Aesthetic startup')

	return app