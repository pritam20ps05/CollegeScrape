from os import environ

mongouri = environ['MONGODB_URI']
secretkey = environ['SECRET_KEY']
mailusername = environ['MAIL_USERNAME']
mailrecipient = environ['MAIL_RECIPIENT']
mailpassword = environ['MAIL_PASSWORD']