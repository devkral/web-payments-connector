
from wtforms import SelectField, ValidationError, validators

from web_payments.forms import PaymentForm
from web_payments import FraudStatus, PaymentStatus

__all__ = ["DummyForm"]

class DummyForm(PaymentForm):
    RESPONSE_CHOICES = (
        ('3ds-disabled', '3DS disabled'),
        ('3ds-redirect', '3DS redirect'),
        ('failure', 'Gateway connection error'),
        ('payment-error', 'Gateway returned unsupported response')
    )
    status = SelectField(choices=PaymentStatus.CHOICES, validators=[validators.InputRequired()])
    fraud_status = SelectField(choices=FraudStatus.CHOICES, validators=[validators.InputRequired()])
    gateway_response = SelectField(choices=RESPONSE_CHOICES, validators=[validators.InputRequired()])
    verification_result = SelectField(choices=PaymentStatus.CHOICES+[("", "")])

    def validate(self):
        if self.gateway_response.data == '3ds-redirect' and not self.verification_result.data:
            self.errors["gateway_response"] = ['When 3DS is enabled you must set post validation status']
        return super().validate()
