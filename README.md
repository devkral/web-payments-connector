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
* (maybe) convert rst to md for documentation like mastodon
* remove support for python2 (it should die)
* integration of none django frameworks like webalchemy (>2)
  * move to WTForms
  * localization: don't use django translation framework (only if used with django)

I hope I can get some help.

Note: I use semantic versioning
