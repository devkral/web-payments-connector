from __future__ import unicode_literals
import os

PROJECT_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), 'payments'))
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')]}]

SECRET_KEY = 'NOTREALLY'
PAYMENT_HOST = 'example.com'

INSTALLED_APPS = ['web_payments', "web_payments_dummy", "web_payments_externalpayments", 'django.contrib.sites']
