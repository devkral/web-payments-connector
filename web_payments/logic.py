import json

from . import FraudStatus, PaymentStatus
from .core import provider_factory

class PaymentAttributeProxy(object):

    def __init__(self, payment):
        self._payment = payment
        super(PaymentAttributeProxy, self).__init__()

    def __getattr__(self, item):
        data = json.loads(self._payment.extra_data or '{}')
        try:
            return data[item]
        except KeyError as e:
            raise AttributeError(*e.args)

    def __setattr__(self, key, value):
        if key == '_payment':
            return super(PaymentAttributeProxy, self).__setattr__(key, value)
        try:
            data = json.loads(self._payment.extra_data)
        except ValueError:
            data = {}
        data[key] = value
        self._payment.extra_data = json.dumps(data)


class BasePaymentLogic(object):
    """ Logic of a Payment object, e.g. for tests """

    def change_status(self, status, message=''):
        '''
        Updates the Payment status and sends the status_changed signal.
        '''
        self.status = status
        self.message = message
        self.save()
        self.signal_status_change()

    def signal_status_change(self):
        """ needs to be overwritten to be useful """
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

    def __unicode__(self):
        return self.variant

    def get_form(self, data=None):
        provider = provider_factory(self.variant)
        return provider.get_form(self, data=data)

    def get_purchased_items(self):
        return []

    def get_failure_url(self):
        raise NotImplementedError()

    def get_success_url(self):
        raise NotImplementedError()

    # needs to be implemented, see BasePaymentWithAddress for an example
    def get_shipping_address(self):
        raise NotImplementedError()

    # needs to be implemented, see BasePaymentWithAddress for an example
    def get_billing_address(self):
        raise NotImplementedError()

    def get_process_url(self):
        raise NotImplementedError()

    def capture(self, amount=None, final=True):
        ''' Capture a fraction of the total amount of a payment. Return amount captured or None '''
        if self.status != PaymentStatus.PREAUTH:
            raise ValueError(
                'Only pre-authorized payments can be captured.')
        provider = provider_factory(self.variant)
        amount = provider.capture(self, amount, final)
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
        provider = provider_factory(self.variant)
        provider.release(self)
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
        provider = provider_factory(self.variant)
        amount = provider.refund(self, amount)
        if amount:
            self.captured_amount -= amount
            if self.captured_amount == 0 and self.status != PaymentStatus.REFUNDED:
                self.change_status(PaymentStatus.REFUNDED)
            self.save()
        return amount

    @classmethod
    def check_token_exists(cls, token):
        return False

    def create_token(self):
        if not self.token:
            tries = {}  # Stores a set of tried values
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

class BasicProvider(object):
    '''
    This class defines the provider API. It should not be instantiated
    directly. Use factory instead.
    '''
    _method = 'post'

    def get_action(self, payment):
        return self.get_return_url(payment)

    def __init__(self, capture=True):
        self._capture = capture

    def get_hidden_fields(self, payment):
        '''
        Converts a payment into a dict containing transaction data. Use
        get_form instead to get a form suitable for templates.

        When implementing a new payment provider, overload this method to
        transfer provider-specific data.
        '''
        raise NotImplementedError()

    def get_form(self, payment, data=None):
        '''
        Converts *payment* into a form suitable for Django templates.
        '''
        from .forms import PaymentForm
        return PaymentForm(self.get_hidden_fields(payment),
                           self.get_action(payment), self._method)

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

    def get_return_url(self, payment, extra_data=None):
        payment_link = payment.get_process_url()
        url = urljoin(get_base_url(), payment_link)
        if extra_data:
            qs = urlencode(extra_data)
            return url + '?' + qs
        return url

    def capture(self, payment, amount=None, final=True):
        ''' Capture a fraction of the total amount of a payment. Return amount captured or None '''
        raise NotImplementedError()

    def release(self, payment):
        ''' Annilates captured payment '''
        raise NotImplementedError()

    def refund(self, payment, amount=None):
        ''' Refund payment, return amount which was refunded '''
        raise NotImplementedError()
