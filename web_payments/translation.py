import os
import gettext
import functools
import threading


__all__ = ["web_payments_translation_path", "set_language", "get_language", "Translation", "translation"]

web_payments_translation_path = os.path.join(os.path.dirname(__file__), "locale")


_tlocal = threading.local()
_tlocal.current_language = "en"

def set_language(lang):
    '''
    Set language. Default implementation
    Note: if get_language is overwritten this method should be also overwritten
    or not used
    Note: loading with django overwrites this method if not initialized
    '''
    _tlocal.current_language = lang

def get_language():
    '''
    Get language. For translations.
    Default implementation can be overwritten.
    Note: if set_language is overwritten this method should be also overwritten
    Note: loading with django overwrites this method if not initialized
    '''
    return _tlocal.current_language

class _lazy_constant(object):
    def __init__(self, func, *args, **kwargs):
        self.func = functools.partial(func, *args, **kwargs)
        # skip partial, provide func
        functools.update_wrapper(self, func)

    def __eq__(self, obj):
        return self.func().__eq__(obj)

    def __ne__(self, obj):
        return self.func().__ne__(obj)

    def __lt__(self, obj):
        return self.func().__lt__(obj)

    def __le__(self, obj):
        return self.func().__le__(obj)

    def __gt__(self, obj):
        return self.func().__gt__(obj)

    def __ge__(self, obj):
        return self.func().__ge__(obj)

    def __str__(self):
        return self.func()

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

    @functools.lru_cache(typed=True)
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
        return _lazy_constant(self.gettext, msg, cur_lang)

    def ngettext_lazy(self, msg, msgplural, n, cur_lang=None):
        return _lazy_constant(self.ngettext, msg, msgplural, n, cur_lang)

translation = Translation(web_payments_translation_path, domain="web_payments")
