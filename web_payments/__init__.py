from collections import namedtuple
from ._exceptions import (RedirectNeeded, ExternalPostNeeded,
                         PaymentError, NotInitialized, NotSupported)
from .status import PaymentStatus, FraudStatus

__all__ = ["PurchasedItem", "HttpRequest"]
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
        PROVIDER_CACHE[name] = class_(**variant.config)
        provextra = PROVIDER_CACHE[name].extra
        PROVIDER_CACHE[name].extra = {}
        if provextra:
            PROVIDER_CACHE[name].extra.update(provextra)
        PROVIDER_CACHE[name].extra.update(variant.extra)
    return PROVIDER_CACHE[name]
