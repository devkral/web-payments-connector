from unittest import TestCase
from unittest.mock import patch, NonCallableMock, MagicMock

from . import get_base_url
from .models import BasePayment
from .urls import process_data, static_callback
from .. import ProviderVariant, PROVIDER_CACHE, PaymentStatus, HttpRequest, RedirectNeeded
from web_payments_dummy import DummyProvider

class TestHelpers(TestCase):
    @patch('django.conf.settings.PAYMENT_HOST', new_callable=NonCallableMock)
    def test_text_get_base_url(self, host):
        host.__str__ = lambda x: "example.com/string"
        self.assertEqual(get_base_url(), "https://example.com/string")

    @patch('django.conf.settings.PAYMENT_HOST')
    def test_callable_get_base_url(self, host):
        host.return_value = "example.com/callable"
        self.assertEqual(get_base_url(), "https://example.com/callable")

    def test_model(self):
        BasePayment.load_providers()
        testp = BasePayment()
        for i in BasePayment.list_providers():
            self.assertIsInstance(i, ProviderVariant)
            self.assertIn(i.extra["name"], PROVIDER_CACHE)
            testp.variant = i.extra["name"]
            self.assertIs(testp.provider, PROVIDER_CACHE[i.extra["name"]])

    # need fixes
    #def test_process(self):
    #    verification_status = PaymentStatus.CONFIRMED
    #    request = MagicMock()
    #    request.GET = {'verification_result': verification_status}
    #    testp = BasePayment(variant="DummyProvider")
    #    with self.assertRaises(RedirectNeeded) as exc:
    #        process_data(testp, request)
    #        self.assertEqual(testp.status, verification_status)
    #        self.assertEqual(exc.args[0], testp.get_success_url())
