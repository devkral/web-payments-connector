
from django.urls import reverse_lazy
from django.views.generic import FormView
from django import forms
from .models import QPayment

class PaymentView(FormView):
    template_name = "form.html"
    def get_form(form_class=None):
        return self.request.session.payment.provider.get_form(self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class SelectPaymentForm(forms.Form):
    variant = forms.ChoiceField(required=True, label="Payment Method")

    def __init__(self, *args, **kwargs):
       super(SelectPaymentForm, self).__init__(*args, **kwargs)
       self.fields['variant'].choices = map(lambda x: (x, _(x)), QPayment.list_providers())

class SelectView(FormView):
    template_name = "form.html"
    success_url = reverse_lazy("payment-form")
    def get_form(self, form_class=None):
        return SelectPaymentForm(**self.get_form_kwargs())
