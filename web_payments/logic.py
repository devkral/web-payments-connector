from uuid import uuid4
from decimal import Decimal


import simplejson as json

from . import NotSupported, FraudStatus, PaymentStatus, ProviderVariant, provider_factory

__all__ = ["BasicPayment", "BasicProvider"]


class PaymentAttributeProxy(object):

    def __init__(self, payment):
        super().__init__()
        self._payment = payment
        # replace
        #payment.__dict__["attrs"] = self

    def __getattr__(self, item):
        data = json.loads(self._payment.extra_data or '{}')
        try:
            return data[item]
        except KeyError as e:
            raise AttributeError(*e.args)

    def __setattr__(self, key, value):
        if key == '_payment':
            return super().__setattr__(key, value)
        try:
            data = json.loads(self._payment.extra_data, use_decimal=True)
        except ValueError:
            data = {}
        data[key] = value
        self._payment.extra_data = json.dumps(data, use_decimal=True)

class BasicPayment(object):
    ''' Logic of a Payment object, basis for implementations '''

    def change_status(self, status, message=''):
        '''
            Updates the Payment status and sends the status_changed signal.
        '''
        self.status = status
        self.message = message
        self.save()
        self.signal_status_change()

    def signal_status_change(self):
        '''
            Called on status change. Should send signal (see django.models for example).
            must to be overwritten to be useful
        '''
        pass

    def change_fraud_status(self, status, message='', commit=True):
        available_statuses = [choice[0] for choice in FraudStatus.CHOICES]
        if status not in available_statuses:
            raise ValueError(
                'Wrong status "%s", it should be one of: %s' % (
                    status, ', '.join(available_statuses)))
        self.fraud_status = status
        self.fraud_message = message
        if commit:
            self.save()

    def __str__(self):
        return self.variant

    def get_form(self, data=None, **kwargs):
        return self.provider.get_form(self, data=data, **kwargs)

    def get_purchased_items(self):
        return []

    def get_failure_url(self):
        '''
            url where customer should be redirected if payment had an error
        '''
        raise NotImplementedError()

    def get_success_url(self):
        '''
            url where customer should be redirected if payment was successful
        '''
        raise NotImplementedError()

    def get_process_url(self, extra_data=None):
        '''
            returns a communication url, should kept secret
            except if provider communication is with customer
        '''
        raise NotImplementedError()

    @classmethod
    def list_providers(cls, **_kwargs):
        ''' returns an iterable with ProviderVariants '''
        raise NotImplementedError()

    def get_provider_variant(self):
        ''' return ProviderVariant for this payment object '''
        raise NotImplementedError()

    @property
    def provider(self):
        ''' returns provider object '''
        try:
            return provider_factory(self.get_provider_variant())
        except (KeyError, AttributeError) as exc:
            raise ValueError("Payment has invalid provider") from exc

    @classmethod
    def load_providers(cls):
        '''
            Load all providers in cache
            Also useful method to check if all providers are valid
        '''
        for i in cls.list_providers():
            provider_factory(i)

    def get_payment_extra(self):
        '''
            extra costs like delivery or tax (required, Decimal), defaults to zero
            Payment message, minimumage,... (not required, provider SHOULD not depend on it)
            Overwrite or extend to be useful

            universal types:
            type: what type is the transaction (official, physical, ...),
                    VALID value can be provider dependent
            message: message for customer
            minimumage: minimum age for customer
        '''
        return {
            "tax": Decimal("0"),
            "delivery": Decimal("0")
        }

    # needs to be implemented, see BasePaymentWithAddress for an example
    def get_shipping_address(self):
        ''' return shipping address '''
        raise NotImplementedError()

    # needs to be implemented, see BasePaymentWithAddress for an example
    def get_billing_address(self):
        ''' return billing address '''
        raise NotImplementedError()

    def capture(self, amount=None, final=True):
        '''
            Capture a fraction of the total amount of a payment.
            Return amount captured or None
        '''
        if self.status != PaymentStatus.PREAUTH:
            raise ValueError(
                'Only pre-authorized payments can be captured.')
        amount = self.provider.capture(self, amount, final)
        if amount:
            self.captured_amount += amount
            if final:
                self.change_status(PaymentStatus.CONFIRMED)
        return amount

    def release(self):
        ''' Annilates captured payment '''
        if self.status != PaymentStatus.PREAUTH:
            raise ValueError(
                'Only pre-authorized payments can be released.')
        self.provider.release(self)
        self.change_status(PaymentStatus.REFUNDED)

    def refund(self, amount=None):
        ''' Refund payment, return amount which was refunded '''
        if self.status != PaymentStatus.CONFIRMED:
            raise ValueError(
                'Only charged payments can be refunded.')
        if amount:
            if amount > self.captured_amount:
                raise ValueError(
                    'Refund amount can not be greater then captured amount')
        amount = self.provider.refund(self, amount)
        if amount:
            self.captured_amount -= amount
            if self.captured_amount == 0 and self.status != PaymentStatus.REFUNDED:
                self.change_status(PaymentStatus.REFUNDED)
            self.save()
        return amount

    @classmethod
    def check_token_exists(cls, token):
        ''' create token for process_url '''
        return False

    def create_token(self):
        if not self.token:
            tries = set()  # Stores a set of tried values
            while True:
                token = str(uuid4())
                if token in tries and len(tries) >= 100:  # After 100 tries we are impliying an infinite loop
                    raise SystemExit('A possible infinite loop was detected')
                else:
                    if not self.check_token_exists(token):
                        self.token = token
                        break
                tries.add(token)

    @property
    def attrs(self):
        return PaymentAttributeProxy(self)

    def save(self, **kwargs):
        ''' save model implementation dependant '''
        raise NotImplementedError()


BasePaymentLogic = BasicPayment


class BasicProvider(object):
    '''
        This class defines the provider API. It should not be instantiated
        directly. Use factory instead.
    '''
    _method = 'post'
    form_class = None

    def __init__(self, capture=True):
        self._capture = capture

    def get_action(self, payment):
        return payment.get_process_url()

    def get_form(self, payment, data=None, **kwargs):
        '''
            Converts *payment* into a form
        '''
        if not self.form_class:
            raise NotSupported("No form class specified")
        return self.form_class(data=data, provider=self, payment=payment, **kwargs)

    def process_data(self, payment, request):
        '''
            Process callback request from a payment provider.
        '''
        raise NotImplementedError()

    def get_token_from_request(self, payment, request):
        '''
            Return payment token from provider request.
        '''
        raise NotImplementedError()

    def capture(self, payment, amount=None, final=True):
        '''
            Capture a fraction of the total amount of a payment.
            Return amount captured or None
        '''
        raise NotImplementedError()

    def release(self, payment):
        ''' Annilates captured payment '''
        raise NotImplementedError()

    def refund(self, payment, amount=None):
        ''' Refund payment, return amount which was refunded '''
        raise NotImplementedError()
