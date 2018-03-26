import re

__all__ = ["split_streetnr", "getter_prefixed_address", "CARD_TYPES", "get_credit_card_issuer"]

_extract_streetnr = re.compile(r"([0-9]+)\s*$")
def split_streetnr(address, fallback=None):
    ret = _extract_streetnr.search(address[-15:])
    if ret:
        return address[:(ret.start()-15)].strip(), ret.group(0)
    else:
        return address.strip(), fallback

def getter_prefixed_address(prefix):
    """ create getter for prefixed address format """
    first_name = "{}_first_name".format(prefix)
    last_name = "{}_last_name".format(prefix)
    address_1 = "{}_address_1".format(prefix)
    address_2 = "{}_address_2".format(prefix)
    email = "{}_email".format(prefix)
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
            "email": getattr(self, email, None),
            "city": getattr(self, city, None),
            "postcode": getattr(self, postcode, None),
            "country_code": getattr(self, country_code, None),
            "country_area": getattr(self, country_area, None)
        }
    return _get_address


CARD_TYPES = [
    (r'^4[0-9]{12}(?:[0-9]{3})?$', 'visa', 'VISA'),
    (r'^5[1-5][0-9]{14}$', 'mastercard', 'MasterCard'),
    (r'^6(?:011|5[0-9]{2})[0-9]{12}$', 'discover', 'Discover'),
    (r'^3[47][0-9]{13}$', 'amex', 'American Express'),
    (r'^(?:(?:2131|1800|35\d{3})\d{11})$', 'jcb', 'JCB'),
    (r'^(?:3(?:0[0-5]|[68][0-9])[0-9]{11})$', 'diners', 'Diners Club'),
    (r'^(?:5[0678]\d\d|6304|6390|67\d\d)\d{8,15}$', 'maestro', 'Maestro')]


def get_credit_card_issuer(number):
    for regexp, card_type, name in CARD_TYPES:
        if re.match(regexp, number):
            return card_type, name
    return None, None
