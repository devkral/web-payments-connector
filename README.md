web-payments-connector
===============

This project is a fork from django-payments because my changes break the whole api and structure.

Features:
* small (later django independent) connector
* shipping and billing address plus better customizable
* migrate from payments name (this name clashes too easily)
* unified testmocks
* can hold bitcoins and weak currencies
* more flexible

Goals:
* (maybe) convert rst to md for documentation like mastodon
* remove python2 cruft
* move from django to be framework agnostic (>2)
  * move to WTForms (or similar)
  * localization: use django translation framework only with django (or switch from it)

Note: I use semantic versioning.

Please test and lock to a version before integrating. Reaching the goals will require some api breaks.

Please create issues and pull requests. I could really use some help and may break an important feature accidentally.
