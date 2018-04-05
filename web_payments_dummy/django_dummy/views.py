from decimal import Decimal

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from wtforms import SelectField, validators, StringField, DecimalField, widgets
from web_payments.forms import PaymentForm
from web_payments.django import get_payment_model
from web_payments import RedirectNeeded

class PaymentView(SuccessMessageMixin, FormView):
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_urls'] = ["", reverse("payment-form"), reverse("select-form")]
        context["mytitle"] = "Payment"
        return context

    def get_form(self, form_class=None):
        payment = get_payment_model().objects.get(id=self.request.session["paymentid"])
        return payment.get_form(self.get_form_kwargs().get("data", None))

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except RedirectNeeded as exc:
            messages.add_message(request, messages.SUCCESS, "Payment redirects to %s" % exc.args[0])
            return HttpResponseRedirect(exc.args[0])

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        try:
            form = self.get_form()
        except RedirectNeeded as exc:
            messages.add_message(request, messages.SUCCESS, "Payment redirects to %s" % exc.args[0])
            return HttpResponseRedirect(exc.args[0])
        #except Exception as exc:
        #    return HttpResponseBadRequest(exc, content_type="text/plain")

        if form.validate():
            messages.add_message(request, messages.SUCCESS, "Payment succeeded")
            return self.form_valid(form)
        else:
            messages.add_message(request, messages.ERROR, "Payment failed")
            return self.form_invalid(form)

class SelectPaymentForm(PaymentForm):
    variant = SelectField("Payment Method", validators=[validators.InputRequired()])
    total = DecimalField("Total amount", validators=[])
    currency = StringField("Currency", validators=[])
    billing_first_name = StringField("First Name", validators=[validators.Length(max=255)])
    billing_last_name = StringField("Last Name", validators=[validators.Length(max=255)])
    billing_address_1 = StringField("Address", validators=[validators.Length(max=255)])
    billing_address_2 = StringField("Address extension", validators=[validators.Length(max=255)])
    billing_email = StringField("Email", widget=widgets.Input("email"), validators=[validators.Length(max=255), validators.Email(), validators.Optional()])
    billing_city = StringField("City", validators=[validators.Length(max=255)])
    billing_postcode = StringField("Post code", validators=[validators.Length(max=20)])
    billing_country_code = StringField("Country code", validators=[validators.Length(min=2, max=2), validators.Optional()])
    billing_country_area = StringField("Country area", validators=[validators.Length(max=255)])


    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.variant.choices = [(x.extra["name"], x.extra.get("localized_name", x.extra["name"])) for x in get_payment_model().list_providers()]

class SelectView(FormView):
    template_name = "form.html"
    success_url = reverse_lazy("payment-form")
    initial = {"currency": "EUR", "total": Decimal("10.0")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_urls'] = ["", reverse("payment-form"), reverse("select-form")]
        context["mytitle"] = "Select"
        return context

    def get_form(self, form_class=None):
        formkwargs = self.get_form_kwargs()
        return SelectPaymentForm(formdata=formkwargs.get("data", None), data=formkwargs["initial"])

    def form_valid(self, form):
        payment = get_payment_model().objects.create(**form.data)
        self.request.session["paymentid"] = payment.id
        return super().form_valid(form)

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
