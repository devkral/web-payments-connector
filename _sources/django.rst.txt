Django Helpers
==============


#. URL callback processor::

      # urls.py
      from django.urls import include, url

      urlpatterns = [
          url('^payments/', include('web_payments.urls'))]

#. Creating a :class:`Payment` model by subclassing more sophisticated :class:`web_payments.django.models.BasePayment` or :class:`web_payments.django.models.BasePaymentWithAddress`::

      # mypaymentapp/models.py
      from decimal import Decimal

      from web_payments import PurchasedItem
      from web_payments.models import BasePayment

      class Payment(BasePayment):

          def get_failure_url(self):
              return 'http://example.com/failure/'

          def get_success_url(self):
              return 'http://example.com/success/'

          def get_purchased_items(self):
              # you'll probably want to retrieve these from an associated order
              yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                                  quantity=9, price=Decimal(10), currency='USD')

   The :meth:`get_purchased_items` method should return an iterable yielding instances of :class:`web_payments.PurchasedItem`.

#. Get Payment object with ``payment.get_form()`` (full view example)::

      # mypaymentapp/views.py
      from django.shortcuts import get_object_or_404, redirect
      from django.template.response import TemplateResponse
      from web_payments import RedirectNeeded
      from web_payments.django import get_payment_model

      def payment_details(request, payment_id):
          payment = get_object_or_404(get_payment_model(), id=payment_id)
          try:
              form = payment.get_form(data=request.POST or None)
          except RedirectNeeded as redirect_to:
              return redirect(redirect_to.args[0])
          return TemplateResponse(request, 'payment.html',
                                  {'form': form, 'payment': payment})

   .. note::

      Please note that :meth:`Payment.get_form` may raise a :exc:`RedirectNeeded` exception.

#. Configuration by ``settings.py``::

      # settings.py
      INSTALLED_APPS = [
          # ...
          'web_payments.django',
          ]

      PAYMENT_HOST = 'localhost:8000'
      PAYMENT_PROTOCOL = "https"
      PAYMENT_MODEL = 'mypaymentapp.Payment'
      # 'default' is used as extras["name"]
      PAYMENT_VARIANTS_API = {
          'default': ('web_payments_dummy.DummyProvider', {}, {"localized_name": "default", "icon": "icon.png"})}

   Variants are named pairs of payment providers, their configuration and extra information.

   .. note::

      Variant names may are used in URLs so it's best to stick to ASCII.

   .. note::

      PAYMENT_HOST can also be a callable object which takes a :class:`web_payments.ProviderVariant`.
