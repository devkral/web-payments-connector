from django.conf.global_settings import *

import os


DEBUG = True

SECRET_KEY = 'NOTREALLY'
PAYMENT_HOST = 'example.com'
PAYMENT_PROTOCOL = 'https'
PAYMENT_MODEL = "django_dummy.QPayment"

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {}, {}),
    'DummyProvider': ('web_payments_dummy.DummyProvider', {}, {}),
    'direct': ('web_payments_externalpayments.DirectPaymentProvider', {}, {}),
    'iban': ('web_payments_externalpayments.BankTransferProvider', {
        "iban": "GL5604449876543210",
        "bic": "DABAIE2D"}, {}
        ),
    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
    }
}

INSTALLED_APPS = ['web_payments_dummy.django_dummy']
