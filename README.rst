======================================
``minews`` / Libre Projects - News
======================================
:Author: Joar Wandborg http://wandborg.se
:License: AGPLv3

Libre Projects news aggregator.

-------------------------------------------------
Is ``minews`` based on/intended to run on Django?
-------------------------------------------------

No, ``minews`` runs on the non-blocking webserver Tornado_. Although we use ``django.utils.text.Truncator()`` to truncate HTML content. It's a fast solution.


.. _Tornado: http://www.tornadoweb.org
