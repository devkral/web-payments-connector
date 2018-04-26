import os
import gettext
import functools
import threading


__all__ = ["web_payments_translation_path", "set_language", "get_language", "Translation", "translation"]

web_payments_translation_path = os.path.join(os.path.dirname(__file__), "locale")

class _TLocal(threading.local):
    def __init__(self, **kwargs):
        super().__init__()
        for key, val in kwargs.items():
            setattr(self, key, val)

_tlocal = _TLocal(current_language="en")

def set_language(language):
    '''
        Set language.
        Default implementation can be overwritten.
        Note: if get_language is overwritten this method should be also overwritten
        or not used
        Note: loading with django overwrites this method if not initialized

        :param str language: language to set to
    '''
    _tlocal.current_language = language

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
        if not callable(func):
            instance_path, func_name = func
            module_path, instance_path = instance_path.rsplit(".", 1)
            module = __import__(
                str(module_path), globals(), locals(), [str(instance_path)])
            instance_ = getattr(module, instance_path)
            func = getattr(instance_, func_name)

        self.func = functools.partial(func, *args, **kwargs)
        # skip partial, provide func
        functools.update_wrapper(self, func)

    def deconstruct(self):
        selfname = ".".join([_lazy_constant.__module__, _lazy_constant.__qualname__])
        args = [(self.func.func.__self__.instance_path, self.func.func.__qualname__.split(".", 1)[1])]
        # python 3.4 compatibility
        for arg in self.func.args:
            args.append(arg)
        return (selfname, args, self.func.keywords)

    def __getattribute__(self, item):
        if item in ("func", "__dict__", "__init__", "deconstruct"):
            return super().__getattribute__(item)
        return self.func().__getattribute__(item)

    def __eq__(self, obj): return self.func().__eq__(obj)
    def __ne__(self, obj): return self.func().__ne__(obj)
    def __lt__(self, obj): return self.func().__lt__(obj)
    def __le__(self, obj): return self.func().__le__(obj)
    def __gt__(self, obj): return self.func().__gt__(obj)
    def __ge__(self, obj): return self.func().__ge__(obj)
    def __iter__(self): return self.func().__iter__()
    def __len__(self): return self.func().__len__()
    def __str__(self): return self.func()
    def __repr__(self): return "'%s'" % self.func()

class Translation(object):
    fallback = None
    domain = None
    instance_path = None
    translation_path = None
    def __init__(self, instance_path, translation_path, domain="web_payments", fallback=None):
        self.translation_path = translation_path
        self.instance_path = instance_path
        self.domain = domain
        if fallback:
            self.fallback = fallback
        else:
            self.fallback = []

    @functools.lru_cache(typed=True)
    def _trans(self, lang):
        if lang:
            return gettext.translation("web_payments", self.translation_path, [lang]+self.fallback, fallback=True)
        return gettext.translation("web_payments", self.translation_path, self.fallback, fallback=True)

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

translation = Translation("web_payments.translation.translation", web_payments_translation_path, domain="web_payments")
