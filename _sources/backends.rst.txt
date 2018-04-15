Basic Backend Definition
========================

Default arguments
-----------------

captured: Default: True, if False enable preauth
time_reserve: Default: timedelta(seconds=0), how many time should a used token have left at least?

Extras
--------------

Extras should not affect Provider, it is only for the integration.
Notable exception is name:
name is used for provider_factory caching

Rational behind this is that providers of the same type but different parameters can exist.

name is set to dictionary key name in django, testcommon and defaults to
Provider Class Name



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
