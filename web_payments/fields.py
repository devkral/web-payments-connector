
import html
from wtforms import widgets, Field


class PlainTextWidget(object):
    """
    """
    def __call__(self, field, value=None, **kwargs):
        if not value:
            value = field._value()
        return widgets.HTMLString('<div {}>{}</div>'.format(widgets.html_params(**kwargs), html.escape(value)))

class TextField(Field):
    widget = PlainTextWidget()
