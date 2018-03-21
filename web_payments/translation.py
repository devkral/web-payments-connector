import os
import gettext
from functools import partial

translation_path = os.path.join(os.path.dirname(__file__), "locale")
translation = gettext.translation("web_payments", translation_path, ["it"],  fallback=True)

def wpgettext(msg):
    return translation.gettext(msg)

def wpngettext(msg, msgplural, n):
    return translation.ngettext(msg, msgplural, n)

def wpgettext_lazy(msg):
    return partial(wpgettext, msg)

def wpngettext_lazy(msg, msgplural, n):
    return partial(wpngettext, msg, msgplural, n)
