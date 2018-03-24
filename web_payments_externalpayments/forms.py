

from wtforms import StringField, ValidationError
from web_payments.fields import TextField
from web_payments.forms import PaymentForm
from .translation import translation
_ = translation.gettext_lazy

class OrderIdForm(PaymentForm):
    # only shown, return is ignored
    order = TextField(label=_("Please supply as reference"))


class IBANBankingForm(PaymentForm):
    # only shown, return is ignored
    iban = TextField(label="IBAN")
    bic = TextField(label="BIC")
    order = TextField(label=_("Please supply as reference"))
