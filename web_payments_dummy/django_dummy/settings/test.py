from . import *

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {}, {}),
    'DummyProvider': ('web_payments_dummy.DummyProvider', {}, {}),
    'direct': ('web_payments_externalpayments.DirectPaymentProvider', {}, {}),
    'iban': ('web_payments_externalpayments.BankTransferProvider', {
        "iban": "GL5604449876543210",
        "bic": "DABAIE2D"}, {}
        ),
    }

PAYMENT_HOST = 'example.com'
PAYMENT_PROTOCOL = 'https'
