
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
        if field.data < datetime.date.today():
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
    def __init__(self, *args, provider=None, payment=None, action='', method='post', **kwargs):
        super().__init__(**kwargs)
        self.action = action
        self.method = method
        self.provider = provider
        self.payment = payment

class CreditCardPaymentForm(PaymentForm):

    number = StringField(_('Card Number'),
        validators=[validators.Length(max=32),
                    validators.InputRequired(), CreditCardNumberValidator()],
        render_kw={'autocomplete': 'cc-number'})

    expiration = DateField(_('Expiration date (YYYY-MM):'),
        validators=[DateValidator()],
        format='%Y-%m',
        render_kw={'autocomplete': 'cc-exp'})

    cvv2 = StringField(
        _('CVV2 Security Number'), validators=[validators.InputRequired(_('Enter a valid security number.')), validators.Regexp('^[0-9]{3,4}$', _('Enter a valid security number.'))],
        description=_(
            'Last three digits located on the back of your card.'
            ' For American Express the four digits found on the front side.'),
        render_kw={'autocomplete': 'cc-csc'})

    def validate_number(self, form, field):
        if get_credit_card_issuer(field.data)[0] not in self.VALID_TYPES:
            raise ValidationError(
                _('We accept only %(valid_types)s') % {"valid_types": ", ".join(self.VALID_TYPES)})


class CreditCardPaymentFormWithName(CreditCardPaymentForm):
    name = StringField(label=_('Name on Credit Card'),
        validators=[validators.Length(max=128)])
