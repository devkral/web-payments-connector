
import json
from uuid import uuid4
from decimal import Decimal

from django.conf import settings
from django.db import models

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .. import FraudStatus, PaymentStatus
from ..logic import BasicPayment
from .signals import status_changed
from .utils import add_prefixed_address
from ..utils import getter_prefixed_address
from ..translation import translation
_ = translation.gettext_lazy

__all__ = ["BasePayment", "BasePaymentWithAddress"]

class BasePayment(models.Model, BasicPayment):
    '''
    Represents a single transaction. Each instance has one or more PaymentItem.
    '''
    variant = models.CharField(max_length=255)
    #: Transaction status
    status = models.CharField(
        max_length=10, choices=PaymentStatus.CHOICES,
        default=PaymentStatus.WAITING)
    fraud_status = models.CharField(
        max_length=10, choices=FraudStatus.CHOICES,
        default=FraudStatus.UNKNOWN)
    fraud_message = models.TextField(blank=True, default='')
    #: Creation date and time
    created = models.DateTimeField(auto_now_add=True)
    #: Date and time of last modification
    modified = models.DateTimeField(auto_now=True)
    #: Transaction ID (if applicable)
    transaction_id = models.CharField(max_length=255, blank=True)
    #: Currency code (may be provider-specific)
    currency = models.CharField(max_length=10)

    #: description of transaction
    description = models.TextField(blank=True, default='')
    #: message for customer
    message = models.TextField(blank=True, default='')
    #ip address of customer, Note: removed (against privacy law (at least in EU))
    ###customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    #: for attrs pseudo dict
    extra_data = models.TextField(blank=True, default='')
    #: secret token (for get_process_url)
    token = models.CharField(max_length=36, blank=True, default='')

    #: Total amount (gross)
    total = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    #: Delivery costs
    delivery = models.DecimalField(
        max_digits=20, decimal_places=8, default=Decimal('0.0'))
    #: Tax
    tax = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    #: captured = current captured amount
    captured_amount = models.DecimalField(
        max_digits=20, decimal_places=8, default=Decimal('0.0'))

    class Meta:
        abstract = True


    def signal_status_change(self):
        status_changed.send(sender=type(self), instance=self)

    @classmethod
    def check_token_exists(cls, token):
        return cls._default_manager.filter(token=token).exists()

    def get_process_url(self):
        return reverse('process_payment', kwargs={'token': self.token})

    def save(self, **kwargs):
        self.create_token()
        return models.Model.save(self, **kwargs)

@add_prefixed_address("billing")
class BasePaymentWithAddress(BasePayment):
    """ Has real billing address + shippingaddress alias on billing address (alias for backward compatibility) """
    get_billing_address = getter_prefixed_address("billing")
    get_shipping_address = get_billing_address

    class Meta:
        abstract = True
