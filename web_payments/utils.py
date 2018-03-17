from datetime import date
import re

from django.utils.translation import ugettext_lazy as _

def get_month_choices():
    month_choices = [(str(x), '%02d' % (x,)) for x in range(1, 13)]
    return [('', _('Month'))] + month_choices


def get_year_choices():
    year_choices = [(str(x), str(x)) for x in range(
        date.today().year, date.today().year + 15)]
    return [('', _('Year'))] + year_choices

_extract_streetnr = re.compile(r"([0-9]+)\s*$")
def split_streetnr(address, fallback=None):
    ret = _extract_streetnr.search(address[-15:])
    if ret:
        return address[:(ret.start()-15)].strip(), ret.group(0)
    else:
        return address.strip(), fallback



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
