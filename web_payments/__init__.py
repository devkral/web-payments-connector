from collections import namedtuple
from .translation import wpgettext_lazy as _

PurchasedItem = namedtuple('PurchasedItem',
                           'name, quantity, price, currency, sku')

default_app_config = 'web_payments.django.apps.WebPaymentsConfig'


class PaymentStatus:
    WAITING = 'waiting'
    PREAUTH = 'preauth'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    REFUNDED = 'refunded'
    ERROR = 'error'
    INPUT = 'input'

    CHOICES = [
        (WAITING, _('Waiting for confirmation')),
        (PREAUTH, _('Pre-authorized')),
        (CONFIRMED, _('Confirmed')),
        (REJECTED, _('Rejected')),
        (REFUNDED, _('Refunded')),
        (ERROR, _('Error')),
        (INPUT, _('Input'))]


class FraudStatus:
    UNKNOWN = 'unknown'
    ACCEPT = 'accept'
    REJECT = 'reject'
    REVIEW = 'review'

    CHOICES = [
        (UNKNOWN, _('Unknown')),
        (ACCEPT, _('Passed')),
        (REJECT, _('Rejected')),
        (REVIEW, _('Review'))]


class RedirectNeeded(Exception):
    pass

class NotInitialized(NotImplementedError):
    pass


class PaymentError(Exception):

    def __init__(self, message, code=None, gateway_message=None):
        super(PaymentError, self).__init__(message)
        self.code = code
        self.gateway_message = gateway_message


class ExternalPostNeeded(Exception):
    pass
