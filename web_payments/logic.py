from uuid import uuid4
from decimal import Decimal
import threading
import logging
import datetime

import simplejson as json

from . import NotSupported, FraudStatus, PaymentStatus, ProviderVariant, provider_factory

__all__ = ["BasicPayment", "BasicProvider"]

# reserve no time, for Provider token
_no_reserve = datetime.timedelta(seconds=0)

class TokenCache(threading.local):
    """
        threadsafe token cache
    """
    expires = None
    token = None


class PaymentAttributeProxy(object):
    """
        Access payment extra attributes like an object
    """
    _payment = None

    def __init__(self, payment=None):
        super().__init__()
        self._payment = payment

    def __get__(self, pay_inst, _payment_cls):
        if self._payment or pay_inst is None:
            return self
        if not hasattr(pay_inst, "_payment_attribute_proxy_instance"):
            pay_inst._payment_attribute_proxy_instance = PaymentAttributeProxy(pay_inst)
        return pay_inst._payment_attribute_proxy_instance

    @staticmethod
    def __set__(pay_inst, value):
        """ can assign dict to attrs; updates extra_data """
        # instance is always a payment object
        # don't use _payment as it could be not initialized yet
        pay_inst.extra_data = json.dumps(value, use_decimal=True)

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
        self.__set__(self._payment, data)

class BasicPayment(object):
    '''
        Logic of a Payment object, basis for implementations
    '''

    #: select payment provider
    variant = NotImplemented
    #: Transaction status
    status = NotImplemented
    #: Transaction status message
    message = NotImplemented

    #: fraud status
    fraud_status = NotImplemented
    #: fraud message
    fraud_message = NotImplemented

    #: for attrs pseudo dict
    extra_data = NotImplemented
    #: secret token (for get_process_url)
    token = NotImplemented
    #: Transaction ID (if applicable)
    transaction_id = NotImplemented

    #: Currency code (may be provider-specific)
    currency = NotImplemented
    #: Total amount (gross)
    total = NotImplemented
    #: captured = current captured amount
    captured_amount = NotImplemented

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
        '''
            returns an iterable with ProviderVariants
            possible keywords:
            name=<variantname>: extract variant, return list with one provider or [], required for static_callback
        '''
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
            Overwrite or extend to add functionality
            universal types:
            type: what type is the transaction (official, physical, ...), VALID value can be provider dependent
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
        if amount is not None:
            self.captured_amount += amount
            if final:
                self.change_status(PaymentStatus.CONFIRMED)
            else:
                self.save()
        return amount

    def release(self):
        ''' Annilates captured payment '''
        if self.status != PaymentStatus.PREAUTH:
            raise ValueError(
                'Only pre-authorized payments can be released.')
        self.provider.release(self)
        self.captured_amount = Decimal("0")
        self.change_status(PaymentStatus.REFUNDED)

    def refund(self, amount=None):
        ''' Refund payment, return amount which was refunded '''
        if self.status not in (PaymentStatus.CONFIRMED, PaymentStatus.REFUNDED) or self.captured_amount == 0:
            raise ValueError(
                'Only charged payments can be refunded.')
        if amount is not None:
            if amount > self.captured_amount:
                raise ValueError(
                    'Refund amount can not be greater than captured amount')
        amount = self.provider.refund(self, amount)
        if amount is not None:
            if amount > self.captured_amount:
                raise ValueError(
                    'Provider returned refund amount can not be greater than captured amount')
            self.captured_amount -= amount
            if self.status != PaymentStatus.REFUNDED:
                self.change_status(PaymentStatus.REFUNDED)
            else:
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

    # auto initializes, see PaymentAttributeProxy
    attrs = PaymentAttributeProxy()

    def save(self, **kwargs):
        ''' save model implementation dependent '''
        raise NotImplementedError()


BasePaymentLogic = BasicPayment


class BasicProvider(object):
    '''
        This class defines the backend provider API. It should not be instantiated directly. Use BasicPayment methods instead.

        :param bool capture: automatic capture of payments, False not supported by all backends
        :param timedelta time_reserve: minimum time left to expire until a new token is requested, defaults to zero
    '''
    form_class = None

    # Replace by dict to provide default arguments, like name for Provider
    # see extra documentation for variant
    extra = None

    def __init__(self, capture=True, time_reserve=_no_reserve):
        self._capture = capture
        self._time_reserve = time_reserve
        self.token_cache = TokenCache()

    @property
    def token(self):
        '''
            Access to authentication token
        '''
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if not self.token_cache.expires or self.token_cache.expires <= now:
            self.token_cache.token, expires = self.get_auth_token(now)
            if not isinstance(expires, datetime.datetime):
                raise TypeError("Invalid expire type (requires datetime):  %s, %s", type(expires), expires)
            self.token_cache.expires = expires-self._time_reserve
            if self.token_cache.expires < now:
                logging.warning("now > expire - time_reserve, new expire date is in the past: %s", self.token_cache.expires)
        return self.token_cache.token

    def get_auth_token(self, now):
        '''
            Takes now, a datetime object with timezone utc, as argument

            Must return (authentication token, datetime when it will expire)

            datetime can be now to disable caching
        '''
        return NotImplemented, now

    def clear_token_cache(self):
        ''' clear token cache '''
        self.token_cache.expires = None
        self.token_cache.token = None

    def get_action(self, payment):
        return ""

    def get_form(self, payment, data=None, **kwargs):
        '''
            Converts *payment* into a form
        '''
        if not self.form_class:
            raise NotSupported("No form class specified")
        return self.form_class(formdata=data, provider=self, payment=payment, **kwargs)

    def process_data(self, payment, request):
        '''
            Process callback request from a payment provider.
            Default: return 404 if somebody tries it
        '''
        return False

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
