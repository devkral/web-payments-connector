from decimal import Decimal

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from wtforms import SelectField, BooleanField, validators, StringField, DecimalField, widgets
from web_payments.forms import PaymentForm
from web_payments.django import get_payment_model
from web_payments import RedirectNeeded, PaymentStatus, FraudStatus

class PaymentObForm(PaymentForm):
    action = SelectField("Action:", validators=[validators.InputRequired()], choices=[('',''),("capture", "capture"), ("refund", "refund"), ("fail", "fail"), ("fraud", "fraud"), ("success", "success")], render_kw={"onchange": "hideunrelated(this.value)"})
    amount = DecimalField("Amount:", validators=[validators.Optional()])
    final = BooleanField("Final?", validators=[validators.Optional()])
    message = StringField("Message:", validators=[validators.Optional()])

class PayObView(FormView):
    template_name = "payob.html"
    success_url = reverse_lazy("select-form")

    def dispatch(self, request, *args, **kwargs):
        self.payment = get_payment_model().objects.get(id=kwargs["id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_is_local'] = True
        context["mytitle"] = "Payment Object: %s" % self.payment.id
        context["payment_fields"] =[(f.verbose_name, getattr(self.payment, f.name)) for f in self.payment._meta.get_fields()]
        context["payoblist"] = get_payment_model().objects.all()
        return context

    def get_form(self, form_class=None):
        return PaymentObForm(formdata=self.get_form_kwargs().get("data", None))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()

        if form.validate():
            messages.add_message(request, messages.SUCCESS, "Payment update successfull")
            return self.form_valid(form)
        else:
            messages.add_message(request, messages.ERROR, "Payment update failed")
            return self.form_invalid(form)

    def form_valid(self, form):
        data = form.data
        if data["action"] == "capture":
            captured = self.payment.capture(data["amount"], data["final"])
            if captured:
                messages.add_message(self.request, messages.SUCCESS, "Captured: %s" % captured)
        elif data["action"] == "refund":
            refunded = self.payment.refund(data["amount"])
            if refunded:
                messages.add_message(self.request, messages.SUCCESS, "Refunded: %s" % refunded)
        elif data["action"] == "fail":
            self.payment.change_status(PaymentStatus.ERROR, data["message"])
        elif data["action"] == "fraud":
            self.payment.change_fraud_status(FraudStatus.REJECT, data["message"])
        elif data["action"] == "success":
            self.payment.change_status(PaymentStatus.CONFIRMED)
        return super().form_valid(form)

class PaymentView(FormView):
    template_name = "form.html"

    def dispatch(self, request, *args, **kwargs):
        self.payment = get_payment_model().objects.get(id=kwargs["id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if not self.payment.provider._capture:
            return reverse("paymentob", kwargs={"id": self.payment.id})
        else:
            return reverse("select-form")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_urls'] = ["", reverse("payment-form", kwargs={"id": self.payment.id}), reverse("select-form")]
        #context["object"] = get_payment_model().objects.get(id=self.kwargs["id"])
        context["payoblist"] = get_payment_model().objects.all()
        context["mytitle"] = "Payment"
        return context

    def get_form(self, form_class=None):
        return self.payment.get_form(self.get_form_kwargs().get("data", None))

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
    initial = {"currency": "EUR", "total": Decimal("10.0")}

    def get_success_url(self):
        return reverse("payment-form", kwargs={"id": self.payment.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_is_local'] = True
        context["mytitle"] = "Select"
        context["payoblist"] = get_payment_model().objects.all()
        return context

    def get_form(self, form_class=None):
        formkwargs = self.get_form_kwargs()
        return SelectPaymentForm(formdata=formkwargs.get("data", None), data=formkwargs["initial"])

    def form_valid(self, form):
        self.payment = get_payment_model().objects.create(**form.data)
        if self.payment.provider._capture:
            self.payment.captured_amount = self.payment.total
            self.payment.save()
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
