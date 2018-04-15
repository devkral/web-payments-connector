
from decimal import Decimal
from .logic import BasicPayment
from . import PaymentStatus, PurchasedItem, ProviderVariant
from .utils import getter_prefixed_address

__all__ = ["create_test_payment"]

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {}, {}),
    'DummyProvider': ('web_payments_dummy.DummyProvider', {}, {"test_var": "test"}),
    'DirectPaymentProvider': ('web_payments_externalpayments.DirectPaymentProvider', {}, {}),
    'iban': ('web_payments_externalpayments.BankTransferProvider', {
        "iban": "GL5604449876543210",
        "bic": "DABAIE2D"}, {"localized_name": "iban"}
        ),
    }

def create_test_payment(PAYMENT_VARIANTS_API=PAYMENT_VARIANTS_API, **attributes):
    class TestPayment(BasicPayment):
        id = 523
        pk = id
        description = 'payment'
        currency = 'USD'
        status = PaymentStatus.WAITING
        message = ""
        token = "354338723"
        total = Decimal(100)
        captured_amount = Decimal("0.0")
        extra_data = ""
        variant = "undefined"
        transaction_id = None

        billing_first_name = "John"
        billing_last_name = "Smith"
        billing_address_1 = "JohnStreet 23"
        billing_address_2 = ""
        billing_city = "Neches"
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

        @staticmethod
        def _list_providers_helper(item):
            _ndict = {"name": item[0]}
            _ndict.update(item[1][2])
            return ProviderVariant(item[1][0], item[1][1], _ndict)

        @classmethod
        def list_providers(cls, **kwargs):
            """ returns an iterable with ProviderVariants """
            if "name" in kwargs:
                if kwargs["name"] in PAYMENT_VARIANTS_API:
                    return [cls._list_providers_helper((kwargs["name"], PAYMENT_VARIANTS_API[kwargs["name"]]))]
                return []
            return map(cls._list_providers_helper, PAYMENT_VARIANTS_API.items())

        def get_provider_variant(self):
            variant_tup = PAYMENT_VARIANTS_API[self.variant]
            variant = ProviderVariant(variant_tup[0], variant_tup[1], {"name": self.variant})
            variant.extra.update(variant_tup[2])
            return variant

        def get_failure_url(self):
            return 'http://cancel.com'

        def get_process_url(self, extra_data=None):
            return 'http://example.com/token'

        def get_success_url(self):
            return 'http://success.com'

        def save(self, **kwargs):
            pass
    # workaround limitation in python
    for key, val in attributes.items():
        setattr(TestPayment, key, val)
    return TestPayment
