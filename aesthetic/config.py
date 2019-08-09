import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
