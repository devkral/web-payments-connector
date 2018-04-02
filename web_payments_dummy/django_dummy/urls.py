"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic import FormView
from django.forms import Form
from web_payments.django import urls, get_payment_model

def PaymentView(FormView):
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

class SelectPaymentForm(Form):
    variant = forms.ChoiceField(choices=map(lambda x: (x, _(x)), variants), required=True, label=_("Payment Method"))

    def __init__(self, *args, choices=None, **kwargs):
       super(SelectPaymentForm, self).__init__(*args, **kwargs)
       if choices:
           self.fields['variant'].choices = map(lambda x: (x, x), filter(lambda x: x in choices, SelectPaymentForm.variants))

def SelectView(FormView):
    template_name = "form.html"
    success_url = reverse_lazy("payment-form")
    def get_form(self, form_class=None):
        return SelectPaymentForm(**self.get_form_kwargs())



urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', urls),
    path('form/', PaymentView.as_view(), name="payment-form"),
    path('', SelectView.as_view(), name="select-form"),
]
