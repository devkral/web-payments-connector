
from urllib.error import URLError
from urllib.parse import urlencode
from django.http import HttpResponseRedirect

from .forms import DummyForm
from web_payments import PaymentError, RedirectNeeded
from web_payments.status import PaymentStatus
from web_payments.logic import BasicProvider

class DummyProvider(BasicProvider):
    '''
    Dummy payment provider
    '''

    def get_form(self, payment, data=None):
        if payment.status == PaymentStatus.WAITING:
            payment.change_status(PaymentStatus.INPUT)
        form = DummyForm(data=data, provider=self,
                         payment=payment)
        #import pdb;
        #pdb.set_trace()
        if form.validate():
            new_status = form.data['status']
            payment.change_status(new_status)
            new_fraud_status = form.cleaned_data['fraud_status']
            payment.change_fraud_status(new_fraud_status)

            gateway_response = form.data['gateway_response']
            verification_result = form.data['verification_result']
            if gateway_response or verification_result:
                if gateway_response == '3ds-disabled':
                    # Standard request without 3DSecure
                    pass
                elif gateway_response == '3ds-redirect':
                    # Simulate redirect to 3DS and get back to normal
                    # payment processing
                    process_url = payment.get_process_url()
                    params = urlencode(
                        {'verification_result': verification_result})
                    redirect_url = '%s?%s' % (process_url, params)
                    raise RedirectNeeded(redirect_url)
                elif gateway_response == 'failure':
                    # Gateway raises error (HTTP 500 for example)
                    raise URLError('Opps')
                elif gateway_response == 'payment-error':
                    raise PaymentError('Unsupported operation')

            if new_status in [PaymentStatus.PREAUTH, PaymentStatus.CONFIRMED]:
                raise RedirectNeeded(payment.get_success_url())
            raise RedirectNeeded(payment.get_failure_url())
        return form

    def process_data(self, payment, request):
        verification_result = request.GET.get('verification_result')
        if verification_result:
            payment.change_status(verification_result)
        if payment.status in [PaymentStatus.CONFIRMED, PaymentStatus.PREAUTH]:
            return HttpResponseRedirect(payment.get_success_url())
        return HttpResponseRedirect(payment.get_failure_url())

    def capture(self, payment, amount=None, final=True):
        payment.change_status(PaymentStatus.CONFIRMED)
        return amount

    def release(self, payment):
        return None

    def refund(self, payment, amount=None):
        return amount or 0
