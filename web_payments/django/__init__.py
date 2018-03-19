from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
# apps clash with 'apps' of module so import as django_apps
from django.apps import apps as django_apps

from .. import core

PAYMENT_HOST = None
PAYMENT_USES_SSL = None

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

def get_base_url(variant=None):
    """
    Returns host url according to project settings. Protocol is chosen by
    checking PAYMENT_USES_SSL variable.
    If PAYMENT_HOST is not specified, gets domain from Sites.
    Otherwise checks if it's callable and returns it's result. If it's not a
    callable treats it as domain.
    """
    from django.contrib.sites.models import Site
    protocol = 'https' if PAYMENT_USES_SSL else 'http'
    if not PAYMENT_HOST:
        current_site = Site.objects.get_current()
        domain = current_site.domain
    elif callable(PAYMENT_HOST):
        domain = PAYMENT_HOST()
    else:
        domain = PAYMENT_HOST
    return '%s://%s' % (protocol, domain)



def load_settings(initialize=None):
    ''' loads settings and sets functions, required for initialization
        default: initialize only if not initialized
     '''
    global PAYMENT_HOST
    global PAYMENT_USES_SSL

    if initialize is None:
        initialize = not core.is_initialized

    if getattr(settings, "PAYMENT_VARIANTS_API", None):
        core.PAYMENT_VARIANTS_API = settings.PAYMENT_VARIANTS_API


    PAYMENT_HOST = getattr(settings, 'PAYMENT_HOST', None)
    if not PAYMENT_HOST:
        if 'django.contrib.sites' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured('The PAYMENT_HOST setting without '
                                       'the sites app must not be empty.')
        from django.contrib.sites.models import Site

    PAYMENT_USES_SSL = getattr(settings, 'PAYMENT_USES_SSL', not settings.DEBUG)


    if initialize:
        core.get_payment_model = get_payment_model
        core.get_base_url = get_base_url
        core.is_initialized = True
