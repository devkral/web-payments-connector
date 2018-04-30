
from decimal import Decimal
from urllib.parse import urlencode, urljoin

from django.db import models
from django.conf import settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .. import FraudStatus, PaymentStatus, ProviderVariant
from ..logic import BasicPayment
from ..utils import getter_prefixed_address
from .signals import status_changed
from . import get_base_url

__all__ = ["BasePayment", "BasePaymentWithAddress"]


class BasePayment(models.Model, BasicPayment):
    '''
    Represents a single transaction. Each instance has one or more PaymentItem.
    '''
    # overwrite variant to remove field
    #: select payment provider
    variant = models.CharField(max_length=255)
    #: Transaction status
    status = models.CharField(
        max_length=10, choices=PaymentStatus.CHOICES,
        default=PaymentStatus.WAITING)
    #: Transaction status message
    message = models.TextField(blank=True, default='')

    #: fraud status
    fraud_status = models.CharField(
        max_length=10, choices=FraudStatus.CHOICES,
        default=FraudStatus.UNKNOWN)
    #: fraud message
    fraud_message = models.TextField(blank=True, default='')

    #: for attrs pseudo dict
    extra_data = models.TextField(blank=True, default='')
    #: secret token (for get_process_url)
    token = models.CharField(max_length=36, blank=True, default='')
    #: Transaction ID (if applicable)
    transaction_id = models.CharField(max_length=255, blank=True)

    #: Currency code (may be provider-specific)
    currency = models.CharField(max_length=10)
    #: Total amount (gross)
    total = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    #: captured = current captured amount
    captured_amount = models.DecimalField(
        max_digits=20, decimal_places=8, default=Decimal('0.0'))

    #: recommended for audit:
    #created = models.DateTimeField(auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def signal_status_change(self):
        status_changed.send(sender=type(self), instance=self)

    def get_process_url(self, extra_data=None):
        url = reverse('process_payment', kwargs={'token': self.token})
        url = urljoin(get_base_url(self.provider), url)
        if extra_data:
            qs = urlencode(extra_data)
            return url + '?' + qs
        return url

    @classmethod
    def list_providers(cls, **kwargs):
        """ returns an iterable with ProviderVariants """
        def _helper(item):
            t = {"name": item[0]}
            t.update(item[1][2])
            return ProviderVariant(item[1][0], item[1][1], t)
        if "name" in kwargs:
            if kwargs["name"] in settings.PAYMENT_VARIANTS_API:
                return [_helper((kwargs["name"], settings.PAYMENT_VARIANTS_API[kwargs["name"]]))]
            else:
                return []
        else:
            return map(_helper, settings.PAYMENT_VARIANTS_API.items())

    @classmethod
    def check_token_exists(cls, token):
        return cls._default_manager.filter(token=token).exists()

    def save(self, **kwargs):
        self.create_token()
        return models.Model.save(self, **kwargs)


class BasePaymentWithAddress(BasePayment):
    """ Has real billing address + shippingaddress alias on billing address """
    get_billing_address = getter_prefixed_address("billing")
    get_shipping_address = get_billing_address

    billing_first_name = models.CharField(max_length=256, blank=True)
    billing_last_name = models.CharField(max_length=256, blank=True)
    billing_address_1 = models.CharField(max_length=256, blank=True)
    billing_address_2 = models.CharField(max_length=256, blank=True)
    billing_email = models.EmailField(blank=True)
    billing_city = models.CharField(max_length=256, blank=True)
    billing_postcode = models.CharField(max_length=20, blank=True)
    billing_country_code = models.CharField(max_length=2, blank=True)
    billing_country_area = models.CharField(max_length=256, blank=True)

    class Meta:
        abstract = True
