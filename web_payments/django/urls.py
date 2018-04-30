'''
This module is responsible for automatic processing of provider callback
data (asynchronous transaction updates).
'''
import logging

import simplejson as json
import xmltodict

from django.http import Http404, HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic
try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from . import get_payment_model
from .. import HttpRequest, RedirectNeeded, provider_factory


def _process_data(request, payment, provider):
    try:
        # request should have some abstraction
        # redefine django request as namedtuple
        # parse most used content types correct
        if request.method == "GET":
            content = None
        elif request.content_type in ("application/json", "application/hal+json"):
            content = json.loads(request.body, use_decimal=True)
        elif request.content_type == "application/x-www-form-urlencoded":
            content = request.POST
        elif request.content_type in ('application/xml', 'application/hal+xml', 'text/xml'):
            # I cannot allow people to handle xml themselves
            # You need good security know-how to handle it
            content = xmltodict.parse(request.body)
        else:
            content = request.body
        reqparsed = HttpRequest(request.method, request.GET, content, request.content_type)
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
        return HttpResponseRedirect(exc.args[0])
    except Exception as exc:
        # for some providers this faces to the banking solution
        # log here for beeing visible
        logging.exception(exc)
        # could contain sensitive data so don't return any information
        # just log
        return HttpResponseServerError()

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
            provider = payment.provider
        except ValueError:
            raise Http404('No such provider')
    return _process_data(request, payment, provider)

@csrf_exempt
@atomic
def static_callback(request, variant):
    Payment = get_payment_model()
    try:
        provider = Payment.get_provider(name=variant)
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
        name='static_process_payment')
    ]
