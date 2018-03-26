from .translation import translation
_ = translation.gettext_lazy

#may better include from web_payments
__all__ = []

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
