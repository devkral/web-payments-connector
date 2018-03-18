Provided backends
=================


Dummy
-----

.. class:: web_payments_dummy.DummyProvider

   This is a dummy backend suitable for testing your store without contacting any payment gateways. Instead of using an external service it will simply show you a form that allows you to confirm or reject the payment.

Example::

      PAYMENT_VARIANTS_API = {
          'dummy': ('web_payments_dummy.DummyProvider', {})}
