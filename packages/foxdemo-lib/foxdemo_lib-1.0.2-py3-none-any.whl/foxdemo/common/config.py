import os

WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
WEB_PORT = os.getenv('WEB_PORT', 8080)

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_USER = os.getenv('MONGO_USER', 'sandbox_user')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'sandbox_password')