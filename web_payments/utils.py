from datetime import date
import re


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
