
import datetime

from wtforms import Form, validators, ValidationError
from wtforms import StringField, DateField
from wtforms.utils import WebobInputWrapper

from .translation import translation
_ = translation.gettext_lazy

from .utils import get_credit_card_issuer, DictInputWrapper

__all__ = ["DateValidator", "CreditCardNumberValidator", "PaymentForm", "CreditCardPaymentForm", "CreditCardPaymentFormWithName"]

class DateValidator(object):
    def __init__(self, message=None):
        if not message:
            message = _('Please enter a valid date.')
        self.message = message
    def __call__(self, form, field):
        data = field.data
        if isinstance(data, str):
            data = datetime.datetime.strptime(data, '%Y-%m').date()
        if not data or data < datetime.date.today():
            raise ValidationError(self.message)

class CreditCardNumberValidator(object):
    def __init__(self, message=None):
        if not message:
            message = _('Please enter a valid card number.')
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
    use always formdata except for defaults.
    formdata of is different to Wtforms as it supports dicts
    '''
    method = 'post'
    action = ''
    provider = None
    payment = None

    class Meta:
        def wrap_formdata(self, form, formdata):
            """ work around wtform implementation """
            if formdata is not None and not hasattr(formdata, 'getlist'):
                if hasattr(formdata, 'getall'):
                    return WebobInputWrapper(formdata)
                elif hasattr(formdata, '__getitem__'): # wtform lacks this
                    return DictInputWrapper(formdata)
                else:
                    raise TypeError("formdata should be a (multi)dict-type wrapper that supports the 'getlist' method")
            return formdata

    def __init__(self, *, provider=None, payment=None, **kwargs):
        kwargs["obj"] = payment
        super().__init__(**kwargs)
        self.provider = provider
        self.payment = payment
        if provider and payment:
            self.action = provider.get_action(payment)

class CreditCardPaymentForm(PaymentForm):
    # which credit card types are accepted?
    VALID_TYPES = None

    number = StringField(label=_('Credit Card Number'),
        validators=[validators.InputRequired(), validators.Length(max=32),
                    CreditCardNumberValidator()],
        render_kw={'autocomplete': 'cc-number'})

    expiration = DateField(label=_('Expiration date (MM/YYYY):'),
        validators=[validators.InputRequired(_('Enter a valid expiration date.')), DateValidator()],
        format='%m/%Y',
        render_kw={'autocomplete': 'cc-exp', 'pattern': '[0-9]{2}/[0-9]{4}'})

    cvv2 = StringField(
        label=_('CVV2 Security Number'), validators=[validators.InputRequired(_('Enter a valid security number.')), validators.Regexp('^[0-9]{3,4}$', message=_('Enter a valid security number.'))],
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
        validators=[validators.Length(max=128)],
        render_kw={'autocomplete': 'cc-name'})
