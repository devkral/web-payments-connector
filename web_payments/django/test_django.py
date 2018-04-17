from unittest import TestCase
from unittest.mock import patch, NonCallableMock, MagicMock

import simplejson as json

from . import get_base_url
from .models import BasePayment
from .urls import _process_data
from .. import ProviderVariant, PROVIDER_CACHE, PaymentStatus, HttpRequest, RedirectNeeded
from web_payments_dummy import DummyProvider

class TestHelpers(TestCase):
    def setUp(self):
        PROVIDER_CACHE.clear()

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


class TestUrl(TestCase):
    def setUp(self):
        PROVIDER_CACHE.clear()

    @patch('web_payments.django.models.BasePayment.get_failure_url')
    @patch('web_payments.django.models.BasePayment.get_success_url')
    @patch('web_payments.django.models.BasePayment.save')
    def test_body(self, save, success, failure):
        success.return_value = "success.example.com"
        failure.return_value = "failure.example.com"
        verification_status = PaymentStatus.CONFIRMED
        request = MagicMock()
        request.GET = {}
        request.method = "POST"
        request.body = json.dumps({'verification_result': verification_status})
        request.content_type = "application/json"
        testp = BasePayment(variant="DummyProvider")
        self.assertEqual(_process_data(request, testp, testp.provider).url, testp.get_success_url())
        self.assertEqual(testp.status, verification_status)

    @patch('web_payments.django.models.BasePayment.get_failure_url')
    @patch('web_payments.django.models.BasePayment.get_success_url')
    @patch('web_payments.django.models.BasePayment.save')
    def test_www(self, save, success, failure):
        success.return_value = "success.example.com"
        failure.return_value = "failure.example.com"
        verification_status = PaymentStatus.CONFIRMED
        request = MagicMock()
        request.GET = {}
        request.method = "POST"
        request.content_type = "application/x-www-form-urlencoded"
        request.POST = {'verification_result': verification_status}
        testp = BasePayment(variant="DummyProvider")
        self.assertEqual(_process_data(request, testp, testp.provider).url, testp.get_success_url())
        self.assertEqual(testp.status, verification_status)

    @patch('web_payments.django.models.BasePayment.get_failure_url')
    @patch('web_payments.django.models.BasePayment.get_success_url')
    @patch('web_payments.django.models.BasePayment.save')
    def test_get(self, save, success, failure):
        success.return_value = "success.example.com"
        failure.return_value = "failure.example.com"
        verification_status = PaymentStatus.CONFIRMED
        request = MagicMock()
        request.GET = {'verification_result': verification_status}
        request.POST = {}
        request.method = "GET"
        request.content_type = None
        testp = BasePayment(variant="DummyProvider")
        self.assertEqual(_process_data(request, testp, testp.provider).url, testp.get_success_url())
        self.assertEqual(testp.status, verification_status)
