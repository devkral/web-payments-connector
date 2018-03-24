
import datetime

from wtforms import Form, validators, ValidationError
from wtforms import StringField, DateField

from .translation import translation
_ = translation.gettext_lazy

from .utils import get_credit_card_issuer

class DateValidator(object):
    def __init__(self, message=None):
        if not message:
            message = _('Please enter a valid date.')
        self.message = message
    def __call__(self, form, field):
        data = field.data
        if isinstance(data, str):
            data = datetime.datetime.strptime(data, '%Y-%m').date()
        if data < datetime.date.today():
            raise ValidationError(self.message)

class CreditCardNumberValidator(object):
    def __init__(self, message=None):
        if not message:
            message = _('Please enter a valid card number')
        self.message = message

    def __call__(self, form, field):
        if not self.cart_number_checksum_validation(field.data):
            raise ValidationError(self.message)

    @staticmethod
    def cart_number_checksum_validation(number):
        digits = []
        even = False
        if not number.isdigit():
            return False
        for digit in reversed(number):
            digit = ord(digit) - ord('0')
            if even:
                digit *= 2
                if digit >= 10:
                    digit = digit % 10 + digit // 10
            digits.append(digit)
            even = not even
        return sum(digits) % 10 == 0 if digits else False

class PaymentForm(Form):
    '''
    Payment form

    When displaying the form remember to use *action* and *method*.
    '''
    method = 'post'
    action = ''
    provider = None
    payment = None

    def __init__(self, *, provider=None, payment=None, **kwargs):
        if "data" not in kwargs:
            kwargs["obj"] = payment
        super().__init__(**kwargs)
        self.provider = provider
        self.payment = payment
        if provider and payment:
            self.action = provider.get_action(payment)

class CreditCardPaymentForm(PaymentForm):
    # which credit card types are accepted?
    VALID_TYPES = None

    number = StringField(label=_('Card Number'),
        validators=[validators.Length(max=32),
                    validators.Required(), CreditCardNumberValidator()],
        render_kw={'autocomplete': 'cc-number'})

    expiration = DateField(label=_('Expiration date (YYYY-MM):'),
        validators=[DateValidator()],
        format='%Y-%m',
        render_kw={'autocomplete': 'cc-exp'})

    cvv2 = StringField(
        label=_('CVV2 Security Number'), validators=[validators.Required(_('Enter a valid security number.')), validators.Regexp('^[0-9]{3,4}$', message=_('Enter a valid security number.'))],
        description=_(
            'Last three digits located on the back of your card.'
            ' For American Express the four digits found on the front side.'),
        render_kw={'autocomplete': 'cc-csc'})

    def __init__(self, *, valid_types=None, **kwargs):
        self.VALID_TYPES = valid_types
        super().__init__(**kwargs)

    def validate_number(self, field):
        if self.VALID_TYPES and get_credit_card_issuer(field.data)[0] not in self.VALID_TYPES:
            raise ValidationError(
                _('We accept only %(valid_types)s') % {"valid_types": ", ".join(self.VALID_TYPES)})


class CreditCardPaymentFormWithName(CreditCardPaymentForm):
    name = StringField(label=_('Name on Credit Card'),
        validators=[validators.Length(max=128)])
