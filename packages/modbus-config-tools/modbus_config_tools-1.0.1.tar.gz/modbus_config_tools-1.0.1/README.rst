modbus_config_tools
======

The basic modbus_config_tools app built in the Flask `tutorial`_.

.. _tutorial: http://flask.pocoo.org/docs/tutorial/


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the master branch. ::

    # clone the repository
    $ git clone git@github.com:shenyunbrother/MY-Flask.git
    $ cd config_studio
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above


Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate

Install modbus_config_tools::

    $ pip install -e .

Or if you are using the master branch, install Flask from source before
installing config_studio::

    $ pip install -e ../..
    $ pip install -e .


Run
---

::

    $ export FLASK_APP=app
    $ export FLASK_ENV=development
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=app
    > set FLASK_ENV=development
    > flask run

    > `waitress-serve --port=8080  --call app:create_app`

Open http://127.0.0.1:8080 in a browser.


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
