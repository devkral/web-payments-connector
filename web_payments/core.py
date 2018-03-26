import re
import threading
from . import NotInitialized

is_initialized = False

PROVIDER_CACHE = {}

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {})}

tlocal = threading.local()
tlocal.current_language = "en"

def set_language(lang):
    '''
    Set language. Default implementation
    Note: if get_language is overwritten this method should be also overwritten
    or not used
    Note: loading with django overwrites this method if not initialized
    '''
    tlocal.current_language = lang

def get_language():
    '''
    Get language. For translations.
    Default implementation can be overwritten.
    Note: if set_language is overwritten this method should be also overwritten
    Note: loading with django overwrites this method if not initialized
    '''
    return tlocal.current_language

def get_base_url(variant=None):
    raise NotInitialized()

def get_payment_model():
    '''
    Return the Payment model of default backend
    '''
    raise NotInitialized()

def provider_factory(variant):
    '''
    Return the provider instance based on variant
    '''
    handler, config = PAYMENT_VARIANTS_API.get(variant, (None, None))
    if not handler:
        raise ValueError('Payment variant does not exist: %s' %
                         (variant,))
    if variant not in PROVIDER_CACHE:
        module_path, class_name = handler.rsplit('.', 1)
        module = __import__(
            str(module_path), globals(), locals(), [str(class_name)])
        class_ = getattr(module, class_name)
        PROVIDER_CACHE[variant] = class_(**config)
    return PROVIDER_CACHE[variant]
