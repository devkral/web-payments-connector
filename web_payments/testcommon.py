
from datetime import datetime
from decimal import Decimal
from .logic import BasicPayment
from . import PaymentStatus, PurchasedItem, ProviderVariant, provider_factory
from .utils import getter_prefixed_address
from functools import partial
from unittest import mock

__all__ = ["create_test_payment"]

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {}, {}),
    'DummyProvider': ('web_payments_dummy.DummyProvider', {}, {}),
    'DirectPaymentProvider': ('web_payments_externalpayments.DirectPaymentProvider', {}, {}),
    'iban': ('web_payments_externalpayments.BankTransferProvider', {
        "iban": "GL5604449876543210",
        "bic": "DABAIE2D"}, {"name": "iban"}
        ),
    }

def create_test_payment(PAYMENT_VARIANTS_API=PAYMENT_VARIANTS_API, **attributes):
    class TestPayment(BasicPayment):
        id = 523
        pk = id
        description = 'payment'
        currency = 'USD'
        delivery = Decimal(10.8)
        status = PaymentStatus.WAITING
        message = ""
        tax = Decimal(10)
        token = "354338723"
        total = Decimal(100)
        captured_amount = Decimal("0.0")
        extra_data = ""
        variant = "undefined"
        transaction_id = None
        created = datetime.now()
        modified = datetime.now()

        billing_first_name = 'John'
        billing_last_name = 'Smith'
        billing_address_1 = 'JohnStreet 23'
        billing_address_2 = ''
        billing_city = 'Neches'
        billing_postcode = "75779"
        billing_country_code = "US"
        billing_country_area = "Tennessee"
        billing_email = "example@example.com"

        get_billing_address = getter_prefixed_address("billing")
        get_shipping_address = get_billing_address

        def __init__(self, **kwargs):
            for key, val in kwargs.items():
                setattr(self, key, val)

        def get_purchased_items(self):
            return [
                PurchasedItem(
                    name='foo', quantity=10, price=Decimal('20'),
                    currency='USD', sku='bar')]

        @classmethod
        def list_providers(cls, **_kwargs):
            """ returns an iterable with ProviderVariants """
            def _helper(item):
                t={"name": item[0]}
                t.update(item[1][2])
                return ProviderVariant(item[1][0], item[1][1], t)
            return map(_helper, PAYMENT_VARIANTS_API.items())

        def get_provider_variant(self):
            variant_tup = PAYMENT_VARIANTS_API[self.variant]
            variant = ProviderVariant(variant_tup[0], variant_tup[1], {"name": self.variant})
            variant.extra.update(variant_tup[2])
            return variant

        def get_failure_url(self):
            return 'http://cancel.com'

        def get_process_url(self, extra_data=None):
            return 'http://example.com'

        def get_success_url(self):
            return 'http://success.com'

        def save(self):
            pass
    # workaround limitation in python
    for key, val in attributes.items():
        setattr(TestPayment, key, val)
    return TestPayment
