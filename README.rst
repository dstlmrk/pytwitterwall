Twitter Wall
============

Download
--------

You can download current version at PyPI_.

.. _PyPI: https://testpypi.python.org/pypi/pytwitterwall/

Usage
-----

.. code::

   Usage: pytwitterwall [OPTIONS] COMMAND [ARGS]...
   
     Simple program which reads posts from Twitter via its API.
   
   Options:
     --conf TEXT                     Configuration path [./conf/auth.cfg].
     --initial-count INTEGER         Count of first tweets [15]. Max 100.
     --retweets-are-allowed / --no-retweets
                                     Flag that shows retweets. Defaults to true.
     --help                          Show this message and exit.

   Commands:
     console  Run the console app
     web      Run the web app

Web app receives search string via url address:

.. code::

   /search/put-your-query


Config file
-----------

You can set access data for your Twitter_ account in configuration file (by default :code:`./conf/auth.cfg`). You should use this pattern:

.. _Twitter: https://twitter.com/

.. code::

   [twitter]
   key = your-api-key
   secret = your-api-secret

Usage examples
--------------

Console
```````
.. code::

   $ pytwitterwall --no-retweets console
   Your query string [#python]:
   ----------
   How to get item's position in a list? #python #list https://t.co/npvrx5fFCs
   ----------
   3 simple things you can do every day to harness the power of #PyCharm keyboard shortcuts
   ...

Web app
```````
.. code::

   $ pytwitterwall web --debug
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger pin code: 133-764-633
   ...

Testing
-------

.. code::

   $ python setup.py test

If you want to test API (current data from server, overwrite cassettes) you have to use access data for Twitter by system variable:

.. code::

   $ export AUTH_FILE="./conf/auth.cfg"


Docs
----

For create docs you have to run :code:`make html` in :code:`/docs` directory.

Requirements
------------

- click
- requests
- Flask
- Jinja2
