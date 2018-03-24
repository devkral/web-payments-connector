'''
This module is responsible for automatic processing of provider callback
data (asynchronous transaction updates).
'''
import logging
from django.http import Http404, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic

try:
    from django.urls import url
except ImportError:
    from django.conf.urls import url
from . import get_payment_model
from ..core import provider_factory


@csrf_exempt
@atomic
def process_data(request, token, provider=None):
    '''
    Calls process_data of an appropriate provider.

    Raises Http404 if variant does not exist.
    '''
    Payment = get_payment_model()
    payment = get_object_or_404(Payment, token=token)
    if not provider:
        try:
            provider = provider_factory(payment.variant)
        except ValueError:
            raise Http404('No such payment')
    try:
        # request should have some abstraction
        # tuple (GET dict, content, content type)
        if request.method == "GET":
            reqparsed = (request.GET, None, None)
        else:
            reqparsed = (request.GET, request.content, request.content_type)
        ret = provider.process_data(payment, reqparsed)
        if ret in (True, False, None):
            status = 200
            if ret is None:
                logging.error("process_data returned None, reached end of function without returning")
                status = 500
            elif not ret:
                status = 404
            return HttpResponse(status=status)
        else:
            content, type = ret
            return HttpResponse(content, type)
    except RedirectNeeded as exc:
        return HttpResponseRedirect(exc)
    except Exception as exc: so just log
        # for some providers this faces to the banking solution
        # log here for beeing visible
        logging.exception(exc)
        # could contain sensitive data so don't return any information
        return HttpResponseServerError()

@csrf_exempt
@atomic
def static_callback(request, variant):

    try:
        provider = provider_factory(variant)
    except ValueError:
        raise Http404('No such provider')

    token = provider.get_token_from_request(request=request, payment=None)
    if not token:
        raise Http404('Invalid response')
    return process_data(request, token, provider)


urlpatterns = [
    url(r'^process/(?P<token>[0-9a-z]{8}-[0-9a-z]{4}-'
        '[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/$', process_data,
        name='process_payment'),
    url(r'^process/(?P<variant>[a-z-]+)/$', static_callback,
        name='static_process_payment')]
