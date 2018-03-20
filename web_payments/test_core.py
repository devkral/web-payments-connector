from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch, NonCallableMock

from . import core
from . import django
from .django.models import BasePayment
from . import PaymentStatus


class TestHelpers(TestCase):
    @patch('web_payments.django.PAYMENT_USES_SSL', new_callable=NonCallableMock)
    @patch('web_payments.django.PAYMENT_HOST', new_callable=NonCallableMock)
    def test_text_get_base_url(self, host, use_ssl):
        host.__str__ = lambda x: "example.com/string"
        use_ssl = False
        self.assertEqual(django.get_base_url(), "https://example.com/string")

    @patch('web_payments.django.PAYMENT_USES_SSL', new_callable=NonCallableMock)
    @patch('web_payments.django.PAYMENT_HOST')
    def test_callable_get_base_url(self, host, use_ssl):
        host.return_value = "example.com/callable"
        use_ssl = False
        self.assertEqual(django.get_base_url(), "https://example.com/callable")


class TestProviderFactory(TestCase):

    def test_provider_factory(self):
        core.provider_factory('default')

    def test_provider_does_not_exist(self):
        self.assertRaises(ValueError, core.provider_factory, 'fake_provider')


class TestBasePayment(TestCase):

    def test_payment_attributes(self):
        payment = BasePayment(
            extra_data='{"attr1": "test1", "attr2": "test2"}')
        self.assertEqual(payment.attrs.attr1, "test1")
        self.assertEqual(payment.attrs.attr2, 'test2')
        self.assertEqual(getattr(payment.attrs, "attr5", None), None)
        self.assertEqual(hasattr(payment.attrs, "attr7"), False)

    def test_capture_with_wrong_status(self):
        payment = BasePayment(variant='default', status=PaymentStatus.WAITING)
        self.assertRaises(ValueError, payment.capture)

    @patch('web_payments_dummy.DummyProvider.capture')
    def test_capture_preauth_successfully(self, mocked_capture_method):
        amount = Decimal('20')
        with patch.object(BasePayment, 'save') as mocked_save_method:
            mocked_save_method.return_value = None
            mocked_capture_method.return_value = amount

            captured_amount = Decimal('0')
            payment = BasePayment(variant='default', captured_amount=captured_amount,
                                  status=PaymentStatus.PREAUTH)
            payment.capture(amount)

            self.assertEqual(payment.status, PaymentStatus.CONFIRMED)
            self.assertEqual(payment.captured_amount, amount)
        self.assertEqual(mocked_capture_method.call_count, 1)

    @patch('web_payments_dummy.DummyProvider.capture')
    def test_capture_preauth_without_amount(self, mocked_capture_method):
        amount = None
        with patch.object(BasePayment, 'save') as mocked_save_method:
            mocked_save_method.return_value = None
            mocked_capture_method.return_value = amount

            captured_amount = Decimal('0')
            status = PaymentStatus.PREAUTH
            payment = BasePayment(variant='default', status=status,
                                  captured_amount=captured_amount)
            payment.capture(amount)

            self.assertEqual(payment.status, status)
            self.assertEqual(payment.captured_amount, captured_amount)
        self.assertEqual(mocked_capture_method.call_count, 1)

    def test_release_with_wrong_status(self):
        payment = BasePayment(variant='default', status=PaymentStatus.WAITING)
        self.assertRaises(ValueError, payment.release)

    @patch('web_payments_dummy.DummyProvider.release')
    def test_release_preauth_successfully(self, mocked_release_method):
        with patch.object(BasePayment, 'save') as mocked_save_method:
            mocked_save_method.return_value = None

            payment = BasePayment(variant='default', status=PaymentStatus.PREAUTH)
            payment.release()
            self.assertEqual(payment.status, PaymentStatus.REFUNDED)
        self.assertEqual(mocked_release_method.call_count, 1)

    def test_refund_with_wrong_status(self):
        payment = BasePayment(variant='default', status=PaymentStatus.WAITING)
        self.assertRaises(ValueError, payment.refund)

    def test_refund_too_high_amount(self):
        payment = BasePayment(variant='default', status=PaymentStatus.CONFIRMED,
                              captured_amount=Decimal('100'))
        self.assertRaises(ValueError, payment.refund, Decimal('200'))

    @patch('web_payments_dummy.DummyProvider.refund')
    def test_refund_without_amount(self, mocked_refund_method):
        refund_amount = None
        with patch.object(BasePayment, 'save') as mocked_save_method:
            mocked_save_method.return_value = None
            mocked_refund_method.return_value = refund_amount

            captured_amount = Decimal('200')
            status = PaymentStatus.CONFIRMED
            payment = BasePayment(variant='default', status=status,
                                  captured_amount=captured_amount)
            payment.refund(refund_amount)
            self.assertEqual(payment.status, status)
            self.assertEqual(payment.captured_amount, captured_amount)
        self.assertEqual(mocked_refund_method.call_count, 1)

    @patch('web_payments_dummy.DummyProvider.refund')
    def test_refund_partial_success(self, mocked_refund_method):
        refund_amount = Decimal('100')
        captured_amount = Decimal('200')
        status = PaymentStatus.CONFIRMED
        with patch.object(BasePayment, 'save') as mocked_save_method:
            mocked_save_method.return_value = None
            mocked_refund_method.return_value = refund_amount

            payment = BasePayment(variant='default', status=status,
                                  captured_amount=captured_amount)
            payment.refund(refund_amount)
            self.assertEqual(payment.status, status)
            self.assertEqual(payment.captured_amount, Decimal('100'))
        self.assertEqual(mocked_refund_method.call_count, 1)

    @patch('web_payments_dummy.DummyProvider.refund')
    def test_refund_fully_success(self, mocked_refund_method):
        refund_amount = Decimal('200')
        captured_amount = Decimal('200')
        with patch.object(BasePayment, 'save') as mocked_save_method:
            mocked_save_method.return_value = None
            mocked_refund_method.return_value = refund_amount

            payment = BasePayment(variant='default', status=PaymentStatus.CONFIRMED,
                                  captured_amount=captured_amount)
            payment.refund(refund_amount)
            self.assertEqual(payment.status, PaymentStatus.REFUNDED)
            self.assertEqual(payment.captured_amount, Decimal('0'))
        self.assertEqual(mocked_refund_method.call_count, 1)
