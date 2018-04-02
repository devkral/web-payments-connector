from web_payments.django.models import BasePayment
from django.urls import reverse

class QPayment(BasePayment):

    def get_success_url(self):
        return reverse("select-form")

    def get_failure_url(self):
        return reverse("select-form")
