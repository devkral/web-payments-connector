from urllib.parse import urljoin

from django.urls import reverse
from django.db import models

from web_payments.django import get_base_url
from web_payments.django.models import BasePaymentWithAddress

class QPayment(BasePaymentWithAddress):
    class Meta:
        ordering = ['-id']
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_success_url(self):
        return urljoin(get_base_url(), reverse("select-form"))

    def get_failure_url(self):
        return urljoin(get_base_url(), reverse("select-form"))
