import re

__all__ = ["split_streetnr", "getter_prefixed_address", "CARD_TYPES", "get_credit_card_issuer"]

_extract_streetnr = re.compile(r"([0-9]+)$")
def split_streetnr(address, fallback=None):
    address = address.strip()
    # to prevent regex attacks, limit to 15 chars
    ret = _extract_streetnr.search(address[-15:])
    if ret:
        # use rstrip because left side is stripped already
        return address[:(ret.start()-15)].rstrip(), ret.group(0)
    else:
        return address, fallback

def getter_prefixed_address(prefix):
    """ create getter for prefixed address format """
    email = "{}_email".format(prefix)
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
            "email": getattr(self, email, None),
            "first_name": getattr(self, first_name, None),
            "last_name": getattr(self, last_name, None),
            "address_1": getattr(self, address_1, None),
            "address_2": getattr(self, address_2, None),
            "city": getattr(self, city, None),
            "postcode": getattr(self, postcode, None),
            "country_code": getattr(self, country_code, None),
            "country_area": getattr(self, country_area, None)
        }
    return _get_address


CARD_TYPES = [
    (re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$'), 'visa', 'VISA'),
    (re.compile(r'^5[1-5][0-9]{14}$'), 'mastercard', 'MasterCard'),
    (re.compile(r'^6(?:011|5[0-9]{2})[0-9]{12}$'), 'discover', 'Discover'),
    (re.compile(r'^3[47][0-9]{13}$'), 'amex', 'American Express'),
    (re.compile(r'^(?:(?:2131|1800|35\d{3})\d{11})$'), 'jcb', 'JCB'),
    (re.compile(r'^(?:3(?:0[0-5]|[68][0-9])[0-9]{11})$'), 'diners', 'Diners Club'),
    (re.compile(r'^(?:5[0678]\d\d|6304|6390|67\d\d)\d{8,15}$'), 'maestro', 'Maestro')]


def get_credit_card_issuer(number):
    for reg, card_type, name in CARD_TYPES:
        if reg.match(number):
            return card_type, name
    return None, None


class DictInputWrapper(object):
    """
    Allows dicts to be provided as formdict
    """

    def __init__(self, _dict):
        self._wrapped = _dict

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def __contains__(self, name):
        return (name in self._wrapped)

    def getlist(self, name, default=None):
        if name in self._wrapped:
            return [self._wrapped[name]]
        else:
            return default
