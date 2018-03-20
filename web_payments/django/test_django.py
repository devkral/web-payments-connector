

from unittest import TestCase
from .forms import CreditCardPaymentFormWithName, PaymentForm

class TestCreditCardPaymentForm(TestCase):

    def setUp(self):
        self.data = {
            'name': 'John Doe',
            'number': '4716124728800975',
            'expiration_0': '5',
            'expiration_1': '2020',
            'cvv2': '123'}

    def test_form_verifies_card_number(self):
        form = CreditCardPaymentFormWithName(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_raises_error_for_invalid_card_number(self):
        data = dict(self.data)
        data.update({'number': '1112223334445556'})
        form = CreditCardPaymentFormWithName(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('number', form.errors)

    def test_form_raises_error_for_invalid_cvv2(self):
        data = dict(self.data)
        data.update({'cvv2': '12345'})
        form = CreditCardPaymentFormWithName(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cvv2', form.errors)


class TestPaymentForm(TestCase):

    def test_form_contains_hidden_fields(self):
        data = {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 'value3',
            'field4': 'value4'}

        form = PaymentForm(data=data, hidden_inputs=True)
        self.assertEqual(len(form.fields), len(data))
        self.assertEqual(form.fields['field1'].initial, 'value1')
