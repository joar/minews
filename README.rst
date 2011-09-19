======================================
``minews`` / Libre Projects - News
======================================
:Author: Joar Wandborg http://wandborg.se
:License: AGPLv3
:State: Unstable

Libre Projects news aggregator.

------------
Dependencies
------------

*   ``django`` - For text truncation
*   ``feedparser`` - For collection of data
*   ``tornado`` - For web serving
*   ``mongodb`` - For storage


------------
Installation
------------

1.  ``git clone git://github.com/jwandborg/minews.git && cd minews``
2.  ``python bootstrap.py && ./bin/buildout``

------------------
Running ``minews``
------------------

To start a web server on port 8080::

    ./bin/serve

To fetch new data from the feeds::

    ./bin/update

------------
Known issues
------------

*   It's not possible to turn off output from ``./bin/update``
*   Complete lack of configuration files. User configuration currently has to be done in the source code.
