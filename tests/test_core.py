from decimal import Decimal
import datetime
import logging
from unittest import TestCase
from unittest.mock import patch, NonCallableMock

from web_payments import provider_factory, PROVIDER_CACHE
from web_payments import PaymentStatus, FraudStatus
from web_payments.forms import CreditCardPaymentFormWithName, PaymentForm
from web_payments import translation
from web_payments.testcommon import create_test_payment

from web_payments_dummy import DummyProvider

BasePayment = create_test_payment()

class TestTranslation(TestCase):
    CHOICES_PaymentStatus = ['Waiting for confirmation', 'Pre-authorized','Confirmed', 'Rejected','Refunded','Error','Input']

    def test_translation(self):
        old_lang = translation.get_language()
        for i in ["de", "en", "ru", "it"]:
            translation.set_language(i)
            self.assertEqual(translation.get_language(), i)
            for count, val in enumerate(PaymentStatus.CHOICES):
                self.assertEqual(val[1], translation.translation.gettext(self.CHOICES_PaymentStatus[count]))
        translation.set_language(old_lang)


class TestProvider(TestCase):

    def setUp(self):
        PROVIDER_CACHE.clear()

    def test_provider_factory(self):
        payment = BasePayment(variant="DummyProvider")
        self.assertEqual(payment.provider, provider_factory(payment.get_provider_variant()))
        payment = BasePayment(variant="iban")
        self.assertEqual(payment.provider, provider_factory(payment.get_provider_variant()))
        payment.load_providers()

    def test_provider_does_not_exist(self):
        payment = BasePayment(variant="fake_provider")
        with self.assertRaises(ValueError):
            payment.provider

    def test_attributes(self):
        payment = BasePayment(variant="DummyProvider")
        self.assertEqual(payment.provider.extra.get("is_dummy", None), True)
        self.assertEqual(payment.provider.extra.get("test_var", None), "test")
        self.assertEqual(payment.provider.extra.get("name", None), "DummyProvider")

    def test_token_cache(self):
        # unittests are singlethreaded so don't lock explicit (speed)
        # anyway token_cache should normally not be accessed outside of token property
        provider = DummyProvider()
        self.assertEqual(provider.token, 1)
        self.assertEqual(provider.token_cache.token, 1)
        expires = provider.token_cache.expires
        provider.clear_token_cache()
        provider.token
        self.assertGreater(provider.token_cache.expires, expires)
        expires = provider.token_cache.expires
        provider.token
        self.assertGreater(provider.token_cache.expires, expires)

    def test_no_token_cache(self):
        provider = DummyProvider()
        provider.token_cache = None
        self.assertEqual(provider.token, 1)
        provider.clear_token_cache()

    @patch('web_payments_dummy.DummyProvider.get_auth_token')
    def test_warning(self, get_auth_token):
        get_auth_token.side_effect = lambda now: (123, now-datetime.timedelta(seconds=3))
        provider = DummyProvider()
        with self.assertLogs(level=logging.WARNING):
            provider.token

class TestBasicPayment(TestCase):

    def test_payment_attributes(self):
        payment = BasePayment(
            extra_data='{"attr1": "test1", "attr2": "test2"}')
        self.assertEqual(payment.attrs.attr1, "test1")
        self.assertEqual(payment.attrs.attr2, 'test2')
        self.assertEqual(getattr(payment.attrs, "attr5", None), None)
        self.assertEqual(hasattr(payment.attrs, "attr7"), False)


    def test_payment_attributes2(self):
        payment = BasePayment()
        payment.attrs = {"attr1": "test1", "attr2": "test2"}
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
    def test_refund_partial_refunded(self, mocked_refund_method):
        refund_amount = Decimal('100')
        captured_amount = Decimal('200')
        status = PaymentStatus.REFUNDED
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


class TestCreditCardPaymentForm(TestCase):

    def setUp(self):
        self.credit_data = {
                'name': 'John Doe',
                'number': '4716124728800975',
                'expiration':  (datetime.datetime.now()+datetime.timedelta(weeks=3*52)).strftime("%m/%Y"),
                'cvv2': '123'}

    def test_form_verifies_card_number(self):
        form = CreditCardPaymentFormWithName(formdata=self.credit_data)
        self.assertTrue(form.validate())

    def test_form_raises_error_for_invalid_card_number(self):
        data = self.credit_data.copy()
        data.update({'number': '1112223334445556'})
        form = CreditCardPaymentFormWithName(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('number', form.errors)

    def test_form_raises_error_for_invalid_cvv2(self):
        data = self.credit_data.copy()
        data.update({'cvv2': '12345'})
        form = CreditCardPaymentFormWithName(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('cvv2', form.errors)
