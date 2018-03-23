import os
import gettext
from functools import partial, lru_cache
from .core import get_language

web_payments_translation_path = os.path.join(os.path.dirname(__file__), "locale")


class Translation(object):
    _fallback = None
    domain = None
    translation_path = None
    def __init__(self, translation_path, domain="web_payments", fallback=None):
        self.translation_path = translation_path
        self.domain = domain
        if fallback:
            self._fallback = fallback
        else:
            self._fallback = []

    @lru_cache(typed=True)
    def _trans(self, lang):
        return gettext.translation("web_payments", self.translation_path, [lang]+self._fallback, fallback=True)

    def trans(self, cur_lang=None):
        if not cur_lang:
            cur_lang = get_language()
        return self._trans(cur_lang)

    def gettext(self, msg, cur_lang=None):
        return self.trans(cur_lang).gettext(msg)

    def ngettext(self, msg, msgplural, n, cur_lang=None):
        return self.trans(cur_lang).ngettext(msg, msgplural, n)

    def gettext_lazy(self, msg, cur_lang=None):
        return partial(self.gettext, msg, cur_lang)

    def ngettext_lazy(self, msg, msgplural, n, cur_lang=None):
        return partial(self.ngettext, msg, msgplural, n, cur_lang)

translation = Translation(web_payments_translation_path, domain="web_payments")
