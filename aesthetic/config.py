import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or '5c404840f211c0609a21a1eaeb5dda44'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or 1