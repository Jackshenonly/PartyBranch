class Config(object):
	DATABASE = 'info.db'
	DEBUG = True
	SECRET_KEY = 'wwos\xce\xd2\xca\xc7\xd2\xbb\xb8\xf6daboo\xc9\xcf\xb5\xc4\xbd\xad\xb0\xb6dld\xb4\xf2'

class DevelopmentConfig(Config):
	UPLOADS_DEFAULT_URL = "http://localhost:9000/"