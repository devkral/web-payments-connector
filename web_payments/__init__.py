from collections import namedtuple
from django.utils.translation import pgettext_lazy

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
        (WAITING, pgettext_lazy('payment status', 'Waiting for confirmation')),
        (PREAUTH, pgettext_lazy('payment status', 'Pre-authorized')),
        (CONFIRMED, pgettext_lazy('payment status', 'Confirmed')),
        (REJECTED, pgettext_lazy('payment status', 'Rejected')),
        (REFUNDED, pgettext_lazy('payment status', 'Refunded')),
        (ERROR, pgettext_lazy('payment status', 'Error')),
        (INPUT, pgettext_lazy('payment status', 'Input'))]


class FraudStatus:
    UNKNOWN = 'unknown'
    ACCEPT = 'accept'
    REJECT = 'reject'
    REVIEW = 'review'

    CHOICES = [
        (UNKNOWN, pgettext_lazy('fraud status', 'Unknown')),
        (ACCEPT, pgettext_lazy('fraud status', 'Passed')),
        (REJECT, pgettext_lazy('fraud status', 'Rejected')),
        (REVIEW, pgettext_lazy('fraud status', 'Review'))]


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
