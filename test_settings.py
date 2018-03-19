from __future__ import unicode_literals
import os

PROJECT_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), 'payments'))
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')]}]

SECRET_KEY = 'NOTREALLY'
PAYMENT_HOST = 'example.com'

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {}),
    'direct': ('web_payments_externalpayments.DirectPaymentProvider', {}),
    'iban': ('web_payments_externalpayments.BankTransferProvider', {
        "iban": "GL5604449876543210",
        "bic": "DABAIE2D"}
        ),
    }

INSTALLED_APPS = ['django.contrib.sites', 'web_payments']
