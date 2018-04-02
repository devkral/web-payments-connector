from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from wtforms import SelectField, validators
from web_payments.forms import PaymentForm

from .models import QPayment

class PaymentView(SuccessMessageMixin, FormView):
    template_name = "form.html"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_urls'] = ["", reverse("payment-form"), reverse("select-form")]
        context["mytitle"] = "Payment"
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_urls'] = ["", reverse("payment-form"), reverse("select-form")]
        return context

    def get_form(form_class=None):
        return self.request.session.payment.provider.get_form(self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.validate():
            messages.add_message(self.request, messages.SUCCESS, "Payment succeeded")
            return self.form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR, "Payment failed")
            return self.form_invalid(form)

class SelectPaymentForm(PaymentForm):
    variant = SelectField("Payment Method", validators=[validators.InputRequired()])

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.variant.choices = [(x.extra["name"], x.extra.get("localized_name", x.extra["name"])) for x in QPayment.list_providers()]

class SelectView(FormView):
    template_name = "form.html"
    success_url = reverse_lazy("payment-form")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_urls'] = ["", reverse("payment-form"), reverse("select-form")]
        context["mytitle"] = "Select"
        return context

    def get_form(self, form_class=None):
        return SelectPaymentForm(formdata=self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
