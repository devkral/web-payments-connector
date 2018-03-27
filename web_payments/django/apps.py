from django.apps import AppConfig
from django.conf import settings

class WebPaymentsConfig(AppConfig):
    name = 'web_payments'
    def ready(self):
        from . import initialize, get_payment_model
        initialize()
        if getattr(settings, "DEBUG", False):
            get_payment_model().load_providers()
