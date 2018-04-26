Basic Backend Definition
========================

Default arguments
-----------------

* captured: Default: True, if False enable preauth
* time_reserve: Default: timedelta(seconds=0), how many time should a used token have left at least?

Extra
--------------

Extra should not affect Provider, it is only for the integration.
Notable exception is name:
name is used for provider_factory caching

Rational behind this is that providers of the same type but different parameters can exist.

name is set to dictionary key name in django, testcommon and defaults to
Provider Class Name

Builtin backends
================

See :doc:`web_payments_dummy` and :doc:`web_payments_externalpayments`

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


.. todo: Further documentation
