Installation
============

#. Install web-payments-connector

   .. code-block:: bash

      $ pip install web-payments-connector


#. Create a :class:`Payment` model by subclassing :class:`web_payments.logic.BasicPayment`::

      from decimal import Decimal

      from web_payments import PurchasedItem
      from web_payments.logic import BasicPayment

      class Payment(BasicPayment):

          def get_failure_url(self):
              # required
              return 'http://example.com/failure/'

          def get_success_url(self):
              # required
              return 'http://example.com/success/'

          def get_process_url(self):
              # required, bank facing url
              return 'http://example.com/process/<token>'

          def get_billing_address(self):
              # required, see testcommon, django
              return {
                      "email": "example@example.com",
                      "first_name": "John",
                      "last_name": "Smith",
                      "address_1": "JohnStreet 23",
                      "address_2": "",
                      "city": "Neches",
                      "postcode": "75779",
                      "country_code": 'US',
                      "country_area": "Tennessee"
                  }

          def get_shipping_address(self):
              # required, see testcommon, django
              return self.get_billing_address()

          @classmethod
          def list_providers(cls, **kwargs):
              # required, see testcommon, django
              return [ProviderVariant("<pythonpath to provider>", {"capture": True}, {"extra_stuff": None, "name": "MyBackend"}),]

          def get_provider_variant(self):
              # required, see testcommon, django
              return ProviderVariant("<pythonpath to provider>", {"capture": True}, {"extra_stuff": None, "name": "MyBackend"})

          def get_payment_extra(self):
              # optional
              return {
                      "tax": Decimal("0"),
                      "delivery": Decimal("0")
                  }

          def get_purchased_items(self):
              # optional, see testcommon
              yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                                  quantity=9, price=Decimal(10), currency='USD')

The :meth:`get_purchased_items` method should return an iterable yielding instances of :class:`web_payments.PurchasedItem`.



#. Write a view that will handle the payment. You can obtain a form instance by passing POST data to ``payment.get_form()``::

      # mypaymentapp/views.py
      ...
      from web_payments import RedirectNeeded

      def func(payment):
          try:
              form = payment.get_form(data=request.POST or None)
          except RedirectNeeded as redirect_to:
              return redirect(redirect_to.args[0])
          return render(request, 'payment.html',
                                  {'form': form, 'payment': payment})

   .. note::

      Please note that :meth:`Payment.get_form` may raise a :exc:`RedirectNeeded` exception.


#. Create a form template

   .. code-block:: html

      <!-- templates/payment.html -->
      <form action="" method="POST">
          {% for field in form %}
              {{ field.label }} <!-- optional -->
              {{ field }}
              <!-- the next step is optional -->
              {% for error in field.errors %}
                  <ul>
                      <li>{{ error }}</li>
                  </ul>
              {% endfor %}
          {% endfor %}
          <p><input type="submit" value="Proceed" /></p>
      </form>
