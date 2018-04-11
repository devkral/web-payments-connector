Basic Backend Definition
========================

Default arguments
-----------------

captured: Default: True, if False enable preauth

Default extras
--------------

name: name for provider_factory caching

Builtin backends
================


Dummy
-----

.. class:: web_payments_dummy.DummyProvider

   This is a dummy backend suitable for testing your store without contacting any payment gateways. Instead of using an external service it will simply show you a form that allows you to confirm or reject the payment.

Example::

      from web_payments import PaymentVariant

      PaymentVariant('web_payments_dummy.DummyProvider', {}, {})



Writing a backend
=================

TODO
