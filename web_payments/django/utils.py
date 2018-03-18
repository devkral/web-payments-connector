from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.db import models


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
