from collections import namedtuple
from ._exceptions import (RedirectNeeded, ExternalPostNeeded,
                         PaymentError, NotInitialized, NotSupported)
from .status import PaymentStatus, FraudStatus

__all__ = ["PurchasedItem", "HttpRequest", "ProviderVariant"]
__all__ += ["PaymentStatus", "FraudStatus"]
__all__ += ["RedirectNeeded", "ExternalPostNeeded"]
__all__ += ["PaymentError", "NotInitialized", "NotSupported"]
__all__ += ["provider_factory"]

PurchasedItem = namedtuple('PurchasedItem',
                           ['name', 'quantity', 'price', 'currency', 'sku'])

HttpRequest = namedtuple('HttpRequest',
                         ['method', 'GET', 'POST', 'content_type'])

# extra is a dictionary
ProviderVariant = namedtuple('ProviderVariant',
                             ['path', 'config', 'extra'])

PROVIDER_CACHE = {}

def provider_factory(variant):
    '''
    Return the provider instance based on ProviderVariant
    '''
    if not variant or None in variant:
        raise ValueError('Payment variant does not exist: %s' %
                         (variant,))
    module_path, class_name = variant.path.rsplit('.', 1)
    name = variant.extra.get("name", class_name)
    if name not in PROVIDER_CACHE:
        module = __import__(
            str(module_path), globals(), locals(), [str(class_name)])
        class_ = getattr(module, class_name)
        provider_instance = class_(**variant.config)
        provextra = provider_instance.extra
        provider_instance.extra = {}
        if provextra:
            provider_instance.extra.update(provextra)
        provider_instance.extra.update(variant.extra)
        PROVIDER_CACHE[name] = provider_instance
    return PROVIDER_CACHE[name]
