Basic Backend Definition
========================

Default arguments
-----------------

captured: Default: True, if False enable preauth

Default extras
--------------

name: name for provider_factory caching, defaults to Provider Name

Builtin backends
================


Dummy
-----

.. class:: web_payments_dummy.DummyProvider

   This is a dummy backend suitable for testing your store without contacting any payment gateways. Instead of using an external service it will simply show you a form that allows you to confirm or reject the payment.


External Payments
-----------------


.. class:: web_payments_externalpayments.DirectPaymentProvider

   This Provider is suitable for manual cashing processes



.. class:: web_payments_externalpayments.BankTransferProvider

  This Provider allows manual bank transactions. It requires a human
  or a program checking the bank transactions

Writing a backend
=================

See testcommon and externalpayments for good examples

TODO: Further documentation
