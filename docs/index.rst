.. pytwitterwall documentation master file, created by
   sphinx-quickstart on Wed Nov  2 13:40:31 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pytwitterwall's documentation
=============================

Pytwitterwall is simple program which reads posts from Twitter via its API.
It can be used as console app or web app (recommended).

Download and installation
-------------------------

First of all, you can download current version at PyPI_. Then in your console run :code:`python setup.py install`. After this step you have to add :ref:`twitter-key` for your Twitter account in configuration file (by default :code:`./conf/auth.cfg`).

.. _PyPI: https://testpypi.python.org/pypi/pytwitterwall/
.. _Twitter: https://twitter.com/

You should use this pattern:

.. code::

   [twitter]
   key = your-api-key
   secret = your-api-secret

Usage
-----

For console usage run :code:`pytwitterwall console` in terminal. For web app run :code:`pytwitterwall web`.
More informations you can get from help :code:`pytwitterwall --help`.

Web app receives on http://127.0.0.1:5000 search string via url address:

.. code::

   /search/put-your-query


Documentation
-------------

Documentation contents:

.. toctree::
   :maxdepth: 2

   twitter
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

