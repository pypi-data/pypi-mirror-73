py_openshowvar
===============

A Python port of KUKA VarProxy client (OpenShowVar).

Python version
===============

Supports 2.6+ / 3.3+, tested at 2.7.11 and 3.6.3.

Install
========

On PYPI: `<https://pypi.python.org/pypi/py-openshowvar>`_

``pip install py_openshowvar``

Usage
======

Module usage:

.. code-block:: python

    >>> from py_openshowvar import openshowvar
    >>> client = openshowvar('192.168.19.132', 7001)
    >>> client.can_connect
    True
    >>> ov = client.read('$OV_PRO', debug=True)
    [DEBUG] (48, 6, 0, 3, '100', '\x00\x01\x01')
    100
    >>> print ov
    100
    >>> client.close()

Built-in shell usage:

.. code-block:: bash

    $ python ./py_openshowvar.py
    IP Address: 192.168.19.132
    Port: 7001

    Connected KRC Name:  "xxxxxxxxxx"

    Input var_name [, var_value]
    (`q` for quit): $OV_PRO
    [DEBUG] (66, 5, 0, 2, '50', '\x00\x01\x01')
    50

    Input var_name [, var_value]
    (`q` for quit): $OV_PRO, 100
    [DEBUG] (67, 6, 1, 3, '100', '\x00\x01\x01')
    100

    Input var_name [, var_value]
    (`q` for quit): q
    Bye

