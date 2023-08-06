Mypy plugin for PYLS
======================

.. image:: https://badge.fury.io/py/pyls-mypy.svg
    :target: https://badge.fury.io/py/pyls-mypy

.. image:: https://travis-ci.org/tomv564/pyls-mypy.svg?branch=master
    :target: https://travis-ci.org/tomv564/pyls-mypy

This is a plugin for the Palantir's Python Language Server (https://github.com/palantir/python-language-server)

It, like mypy, requires Python 3.2 or newer.


Installation
------------

Install into the same virtualenv as pyls itself.

``pip install pyls-mypy``

Configuration
-------------

``live_mode`` (default is True) provides type checking as you type. This writes a tempfile every time a check is done.

Turning off live_mode means you must save your changes for mypy diagnostics to update correctly.

Depending on your editor, the configuration should be roughly like this:

::

    "pyls":
    {
        "plugins":
        {
            "pyls_mypy":
            {
                "enabled": true,
                "live_mode": true
            }
        }
    }
