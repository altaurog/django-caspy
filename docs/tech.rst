Hacking Caspy
==============

Caspy is built with the following:

    * Python 3.3 (will retain support for 2.7 and 3.2 while convenient)
    * Django 1.7+ (will retain support for 1.4+ while convenient)
    * Django Rest Framework 3.0.x
    * Angular 1.3
    * (select css framework?)
    * likely pandas and matplotlib
    * possibly coffeescript
    * probably sass

Platform independence is desired on all three tiers.
We aim to support:

    * All django-supported database platforms
    * All python-supported server platforms
    * IE9+, Firefox, Safari, Chrome

Testing:

    * factory_boy_
    * PyHamcrest_?
    * coverage.py_
    * py.test and tox
    * CI: drone.io (also bitbucket) or travis-ci.org (github only)
    * See also: `TDD w/ Python`_, `Practical Django Testing`_

.. _factory_boy: https://github.com/rbarrois/factory_boy
.. _coverage.py: http://nedbatchelder.com/code/coverage/
.. _PyHamcrest: https://github.com/hamcrest/PyHamcrest
.. _TDD w/ Python: http://chimera.labs.oreilly.com/books/1234000000754/pt01.html
.. _Practical Django Testing: http://django-testing-docs.readthedocs.org/en/latest/views.html
