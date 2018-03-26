from collections import namedtuple
from ._exceptions import (RedirectNeeded, ExternalPostNeeded,
                         PaymentError, NotInitialized, NotSupported)
from .status import PaymentStatus, FraudStatus

__all__ = ["PurchasedItem", "HttpRequest"]
__all__ += ["PaymentStatus", "FraudStatus"]
__all__ += ["RedirectNeeded", "ExternalPostNeeded"]
__all__ += ["PaymentError", "NotInitialized", "NotSupported"]

PurchasedItem = namedtuple('PurchasedItem',
                           ['name', 'quantity', 'price', 'currency', 'sku'])

HttpRequest = namedtuple('HttpRequest',
                         ['method', 'GET', 'POST', 'content_type'])

# for django
default_app_config = 'web_payments.django.apps.WebPaymentsConfig'
