web-payments-connector
======================

This project is a fork from django-payments. Because the whole structure changes backward incompatible,
I forked.

Features:
* small framework agnostic connector
* more flexible
  * shipping and billing address
  * addresses generated by function; this allows reuse of other framework components
  * dynamic url generation
* migrate from payments name (this name clashes too easily)
* better test facilities
* can hold bitcoins and weak currencies
* more security features (safe xml parsing, hidden credentials)
* framework independent translation
* better documented API (source code)

TODO:
* porting backends
* documentation for version 2.1

Note: I use semantic versioning.
