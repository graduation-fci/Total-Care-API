import os
from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ["64.225.110.140",
                 "http://64.225.110.140/"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'totalcareapiprod',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': ''
    }
}

# (DOMAIN)= ('example.com')