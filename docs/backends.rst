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

See testcommon and externalpayments for good examples.

   .. note:

      as Form Class PaymentForm should be used. It has some tweaks to ease testing and implementation (allowing dicts as formdata input, special attributes)


Test project
------------
For developing a backend a test project exists. It's located in web_payments_dummy/django_dummy.

#. Example: run server::

   .. code-block:: bash
   ./web_payments_dummy/django_dummy/manage.py runserver

Adding your own backends can be done with the DJANGO_SETTINGS_MODULE environment variable and
point to your own settings.
Own settings can live in the settings folder (gitignored) and inherit from web_payments_dummy.django_dummy.settings (for defaults)


TODO: Further documentation
