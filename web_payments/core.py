from . import NotInitialized

__all__ = ["PAYMENT_VARIANTS_API", "get_base_url", "get_payment_model", "provider_factory"]

is_initialized = False

PROVIDER_CACHE = {}

PAYMENT_VARIANTS_API = {
    'default': ('web_payments_dummy.DummyProvider', {})}

def get_base_url(variant=None):
    '''
    """
    Returns host url according to project settings.
    Overwrite if not using django or overwrite get_process_url in Payment
    """
    '''
    raise NotInitialized()

def get_payment_model():
    '''
    Return the Payment model of default backend
    Overwrite if not using django
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
