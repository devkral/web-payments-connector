from wtforms import StringField, ValidationError
from web_payments.forms import PaymentForm
from .translation import translation
_ = translation.gettext_lazy

__all__ = ["OrderIdForm", "IBANBankingForm"]

class OrderIdForm(PaymentForm):
    # only shown, return is ignored
    order = StringField(label=_("Please supply as reference"), render_kw={"readonly": True})


class IBANBankingForm(PaymentForm):
    # only shown, return is ignored
    iban = StringField(label="IBAN", render_kw={"readonly": True})
    bic = StringField(label="BIC", render_kw={"readonly": True})
    order = StringField(label=_("Please supply as reference"), render_kw={"readonly": True})
