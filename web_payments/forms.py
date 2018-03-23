from wtforms import form
from .fields import (CreditCardNumberField, CreditCardExpiryField,
                     CreditCardVerificationField, CreditCardNameField)

from .translation import gettext as _

class PaymentForm(form.Form):
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

    number = CreditCardNumberField(label=_('Card Number'), max_length=32,
                                   required=True)
    expiration = CreditCardExpiryField()
    cvv2 = CreditCardVerificationField(
        label=_('CVV2 Security Number'), required=False, help_text=_(
            'Last three digits located on the back of your card.'
            ' For American Express the four digits found on the front side.'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args,  **kwargs)
        if hasattr(self, 'VALID_TYPES'):
            self.fields['number'].valid_types = self.VALID_TYPES


class CreditCardPaymentFormWithName(CreditCardPaymentForm):

    name = CreditCardNameField(label=_('Name on Credit Card'), max_length=128)

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self._fields.move_to_end(, last=False)
