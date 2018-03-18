from django.apps import AppConfig
from .. import core

class WebPaymentsConfig(AppConfig):
    name = 'web_payments'
    def ready(self):
        if not core.is_initialized:
            from . import load_settings
            load_settings(True)
