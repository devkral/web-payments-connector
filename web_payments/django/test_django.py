from unittest import TestCase
from unittest.mock import patch, NonCallableMock

from . import get_base_url

class TestHelpers(TestCase):
    @patch('web_payments.django.PAYMENT_USES_SSL', new_callable=NonCallableMock)
    @patch('web_payments.django.PAYMENT_HOST', new_callable=NonCallableMock)
    def test_text_get_base_url(self, host, use_ssl):
        host.__str__ = lambda x: "example.com/string"
        use_ssl = False
        self.assertEqual(get_base_url(), "https://example.com/string")

    @patch('web_payments.django.PAYMENT_USES_SSL', new_callable=NonCallableMock)
    @patch('web_payments.django.PAYMENT_HOST')
    def test_callable_get_base_url(self, host, use_ssl):
        host.return_value = "example.com/callable"
        use_ssl = False
        self.assertEqual(get_base_url(), "https://example.com/callable")
