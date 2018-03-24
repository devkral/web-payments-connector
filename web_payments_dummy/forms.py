
from wtforms import SelectField, ValidationError, validators

from web_payments.forms import PaymentForm
from web_payments.status import FraudStatus, PaymentStatus


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
    verification_result = SelectField(choices=PaymentStatus.CHOICES)

    def validate(self):
        gateway_response = self.gateway_response.data
        verification_result = self.verification_result.data
        if gateway_response == '3ds-redirect' and not verification_result:
            self.errors["gateway_response"] = ['When 3DS is enabled you must set post validation status']
        return super().validate()
