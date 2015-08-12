Hacking Caspy
==============

Platform
--------

Caspy is built with the following:

    * Python 3.3 (will retain support for 2.7 and 3.2 while convenient)
    * Django 1.8+ (will retain support for 1.6+ while convenient)
    * Django Rest Framework 3.0.x
    * Angular 1.4
    * (select css framework?)

Platform independence is desired on all three tiers.
We aim to support:

    * All django-supported database platforms
    * All python-supported server platforms
    * IE9+, Firefox, Safari, Chrome

Testing:
--------

We aim for full test coverage on both front and back ends,
but currently only have tests for back end:

    * factory_boy_ (minimally; proved not to be very useful)
    * coverage.py_
    * py.test and tox
    * CI: travis-ci.org

.. _factory_boy: https://github.com/rbarrois/factory_boy
.. _coverage.py: http://nedbatchelder.com/code/coverage/
