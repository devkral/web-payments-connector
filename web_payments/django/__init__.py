from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
# apps clash with 'apps' of module so import as django_apps
from django.apps import apps as django_apps
from django.utils import translation as django_translation

from .. import translation


__all__ = ["get_base_url", "get_payment_model", "initialize"]

# django variable: allows import of web_payments.django instead of full path
default_app_config = 'web_payments.django.apps.WebPaymentsConfig'


def get_payment_model():
    '''
        Return the Payment model that is active in this project
    '''
    try:
        app_label, model_name = settings.PAYMENT_MODEL.split('.')
    except (ValueError, AttributeError):
        raise ImproperlyConfigured('PAYMENT_MODEL must be of the form '
                                   '"app_label.model_name"')
    payment_model = django_apps.get_model(app_label, model_name)
    if payment_model is None:
        msg = (
            'PAYMENT_MODEL refers to model "%s" that has not been installed' %
            settings.PAYMENT_MODEL)
        raise ImproperlyConfigured(msg)
    return payment_model


def get_base_url(provider=None):
    '''
        Returns host url according to project settings. Protocol is chosen by
        PAYMENT_PROTOCOL variable.
        If PAYMENT_HOST is not specified, get domain from Sites.
        Otherwise checks if it's callable and returns it's result. If it's not a
        callable treats it as domain.
    '''
    protocol = getattr(settings, 'PAYMENT_PROTOCOL', 'https')
    PAYMENT_HOST = getattr(settings, 'PAYMENT_HOST', None)
    if not PAYMENT_HOST:
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        domain = current_site.domain
    elif callable(PAYMENT_HOST):
        domain = PAYMENT_HOST(provider)
    else:
        domain = PAYMENT_HOST
    return '%s://%s' % (protocol, domain)


def initialize():
    ''' overwrites get/set language with django equivalents '''
    translation.get_language = django_translation.get_language
    translation.set_language = django_translation.activate
