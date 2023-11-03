from django.apps import AppConfig
from django.conf import settings


class WebPaymentsConfig(AppConfig):
    name = "web_payments"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import get_payment_model, initialize

        initialize()
        if getattr(settings, "DEBUG", False):
            get_payment_model().load_providers()
