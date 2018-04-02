from django.apps import AppConfig
from django.conf import settings

import os

class DummyPaymentsConfig(AppConfig):
    name = 'web_payments_dummy'
    path = os.path.join(settings.BASE_DIR, "web_payments_dummy", "django_dummy")
