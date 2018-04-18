from .translation import translation
_ = translation.gettext_lazy

#may better include from web_payments
__all__ = []

class PaymentStatus:
    WAITING = 'waiting'
    PREAUTH = 'preauth'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected' # end status
    REFUNDED = 'refunded' # end status
    ERROR = 'error' # end status
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
    ACCEPT = 'accept' # end status
    REJECT = 'reject' # end status
    REVIEW = 'review'

    CHOICES = [
        (UNKNOWN, _('Unknown')),
        (ACCEPT, _('Passed')),
        (REJECT, _('Rejected')),
        (REVIEW, _('Review'))]
