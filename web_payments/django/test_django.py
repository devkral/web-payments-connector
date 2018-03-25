from unittest import TestCase
from unittest.mock import patch, NonCallableMock

from . import get_base_url

class TestHelpers(TestCase):
    @patch('django.conf.settings.PAYMENT_HOST', new_callable=NonCallableMock)
    def test_text_get_base_url(self, host):
        host.__str__ = lambda x: "example.com/string"
        self.assertEqual(get_base_url(), "https://example.com/string")

    @patch('django.conf.settings.PAYMENT_HOST')
    def test_callable_get_base_url(self, host):
        host.return_value = "example.com/callable"
        self.assertEqual(get_base_url(), "https://example.com/callable")
