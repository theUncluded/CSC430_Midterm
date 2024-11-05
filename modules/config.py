from modules import model

class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = True
	SQLALCHEMY_DATABASE_URI = model.ENGINE_STRING
	#SECRET_KEY = os.getenv("SECRETKEY") <-fake sec key 
	CSRF_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True