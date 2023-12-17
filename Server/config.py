#SQLALCHEMY_DATABASE_URI = 'sqlite:///../Server/Database/ticketshow.sqlite3'
SQLALCHEMY_DATABASE_URI = 'sqlite:///ticketshow.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY ='THis_IS_very_&very_secret_key'
JWT_SECRET_KEY = "secret&@key"
JWT_ACCESS_TOKEN_EXPIRES = 3600
WTF_CSRF_ENABLED = False
SECURITY_PASSWORD_SALT = 'salt'
SECURITY_ENABLE_ROLE_MANAGEMENT = True
#UPLOAD_FOLDER = "/Server/static/img/Movies"
UPLOAD_FOLDER = '/mnt/c/users/sheth/Desktop/MAD2Proj/Server/static/img/Movies'
CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAAAlSrl130/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=yKu7DsaDoA_7sA0R8TcQIhfeK_eGhb226W8Ll7KHL_Q'
CACHE_TYPE = 'RedisCache'
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379

#TEMPLATE_LOCATION = '/mnt/c/users/sheth/Desktop/MAD2Proj/Server/template'

""" CORS_ALLOW_ORIGIN = "http://localhost:8080"
CORS_ALLOW_METHODS = ['POST', 'GET']
CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization'] """