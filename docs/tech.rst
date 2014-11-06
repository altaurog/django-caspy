Hacking Caspy
==============

Caspy is built with the following:

    * Python 3.3
    * Django 1.7
    * Django Rest Framework
    * Angular 1.3
    * (select css framework?)
    * likely pandas and matplotlib
    * maybe coffeescript or icedcoffee
    * maybe sass

Platform independence is desired on all three tiers.
We aim to support:

    * All django-supported database platforms
    * All python-supported server platforms
    * IE9+, Firefox, Safari, Chrome

Testing:

    * lettuce_ or behave_
    * factory_boy_
    * PyHamcrest_?
    * coverage.py_
    * possibly nose or test.py?
    * See also: `TDD w/ Python`_, `Practical Django Testing`_

.. _lettuce: https://github.com/gabrielfalcao/lettuce
.. _behave: https://github.com/behave/behave
.. _factory_boy: https://github.com/rbarrois/factory_boy
.. _coverage.py: http://nedbatchelder.com/code/coverage/
.. _PyHamcrest: https://github.com/hamcrest/PyHamcrest
.. _TDD w/ Python: http://chimera.labs.oreilly.com/books/1234000000754/pt01.html
.. _Practical Django Testing: http://django-testing-docs.readthedocs.org/en/latest/views.html
