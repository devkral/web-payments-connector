web-payments-connector
===============

This project is a fork from django-payments because I could not get my patches upstream and had
some projects and providers depending on it.
I hope I can create a successful fork and clean some ugly parts up.

Goals:
* small connector (this is why I have connector in the name)
* configurable address stuff
* migrate from payments name (this name clashes easily)
* unify testmocks
* remove support for python2 (it should die)
* maybe someday integration of none django frameworks like webalchemy
  * move to WTForms

I hope I can get some help.
