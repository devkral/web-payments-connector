from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.db import models
try:
    from django.db.models import get_model
except ImportError:
    from django.apps import apps
    get_model = apps.get_model

def get_payment_model():
    '''
    Return the Payment model that is active in this project
    '''
    try:
        app_label, model_name = settings.PAYMENT_MODEL.split('.')
    except (ValueError, AttributeError):
        raise ImproperlyConfigured('PAYMENT_MODEL must be of the form '
                                   '"app_label.model_name"')
    payment_model = get_model(app_label, model_name)
    if payment_model is None:
        msg = (
            'PAYMENT_MODEL refers to model "%s" that has not been installed' %
            settings.PAYMENT_MODEL)
        raise ImproperlyConfigured(msg)
    return payment_model


def getter_prefixed_address(prefix):
    """ create getter for prefixed address format """
    first_name = "{}_first_name".format(prefix)
    last_name = "{}_last_name".format(prefix)
    address_1 = "{}_address_1".format(prefix)
    address_2 = "{}_address_2".format(prefix)
    city = "{}_city".format(prefix)
    postcode = "{}_postcode".format(prefix)
    country_code = "{}_country_code".format(prefix)
    country_area = "{}_country_area".format(prefix)
    def _get_address(self):
        return {
            "first_name": getattr(self, first_name, None),
            "last_name": getattr(self, last_name, None),
            "address_1": getattr(self, address_1, None),
            "address_2": getattr(self, address_2, None),
            "city": getattr(self, city, None),
            "postcode": getattr(self, postcode, None),
            "country_code": getattr(self, country_code, None),
            "country_area": getattr(self, country_area, None)}
    return _get_address

def add_prefixed_address(prefix):
    """ add address with prefix to class """
    first_name = "{}_first_name".format(prefix)
    last_name = "{}_last_name".format(prefix)
    address_1 = "{}_address_1".format(prefix)
    address_2 = "{}_address_2".format(prefix)
    city = "{}_city".format(prefix)
    postcode = "{}_postcode".format(prefix)
    country_code = "{}_country_code".format(prefix)
    country_area = "{}_country_area".format(prefix)
    def class_to_customize(dclass):
        setattr(dclass, first_name, models.CharField(max_length=256, blank=True))
        setattr(dclass, last_name, models.CharField(max_length=256, blank=True))
        setattr(dclass, address_1, models.CharField(max_length=256, blank=True))
        setattr(dclass, address_2, models.CharField(max_length=256, blank=True))
        setattr(dclass, city, models.CharField(max_length=256, blank=True))
        setattr(dclass, postcode, models.CharField(max_length=256, blank=True))
        setattr(dclass, country_code, models.CharField(max_length=2, blank=True))
        setattr(dclass, country_area, models.CharField(max_length=256, blank=True))
        return dclass
    return class_to_customize
