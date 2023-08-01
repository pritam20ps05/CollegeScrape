import pymongo
from os import environ

secretkey = environ['SECRET_KEY']
mongouri = environ['MONGODB_URI']

mailusername = environ['MAIL_USERNAME']
mailrecipient = environ['MAIL_RECIPIENT']
mailpassword = environ['MAIL_PASSWORD']

auth0client_id = environ['AUTH0_CLIENT_ID']
auth0client_secret = environ['AUTH0_CLIENT_SECRET']
auth0domain = environ['AUTH0_DOMAIN']

client = pymongo.MongoClient(mongouri)
datetime_format = '%d-%m-%Y %H:%M:%S'