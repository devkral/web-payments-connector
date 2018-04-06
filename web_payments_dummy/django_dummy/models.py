from urllib.parse import urljoin
from web_payments.django import get_base_url
from web_payments.django.models import BasePaymentWithAddress
from django.urls import reverse

class QPayment(BasePaymentWithAddress):

    def get_success_url(self):
        return urljoin(get_base_url(), reverse("select-form"))

    def get_failure_url(self):
        return urljoin(get_base_url(), reverse("select-form"))
